#!/usr/bin/env python3

# Copyright (C) The btclib developers
#
# This file is part of btclib. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution.
#
# No part of btclib including this file, may be copied, modified, propagated,
# or distributed except according to the terms contained in the LICENSE file.
"""Elliptic curve classes and functions."""
from __future__ import annotations

import json
from math import sqrt
from os import path
from typing import Sequence

from btclib.alias import Integer, Point
from btclib.ec import libsecp256k1
from btclib.ec.curve_group import (
    HEX_THRESHOLD,
    CurveGroup,
    _double_mult,
    _mult,
    _multi_mult,
    jac_from_aff,
)
from btclib.exceptions import BTClibValueError
from btclib.utils import hex_string, int_from_integer


class CurveSubGroup(CurveGroup):
    """Subgroup of the points of an elliptic curve over Fp generated by G."""

    def __init__(self, p: Integer, a: Integer, b: Integer, G: Point) -> None:
        super().__init__(p, a, b)

        # 2. check that xG and yG are integers in the interval [0, p−1]
        # 4. Check that yG^2 = xG^3 + a*xG + b (mod p)
        if len(G) != 2:
            raise BTClibValueError("generator must a be a sequence[int, int]")
        self.G = (int_from_integer(G[0]), int_from_integer(G[1]))
        if not self.is_on_curve(self.G):
            raise BTClibValueError("Generator is not on the curve")
        self.GJ = self.G[0], self.G[1], 1  # Jacobian coordinates

    def __str__(self) -> str:
        result = super().__str__()
        if self.p > HEX_THRESHOLD:
            result += f"\n x_G = {hex_string(self.G[0])}"
            result += f"\n y_G = {hex_string(self.G[1])}"
        else:
            result += f"\n x_G = {self.G[0]}"
            result += f"\n y_G = {self.G[1]}"
        return result

    def __repr__(self) -> str:
        result = super().__repr__()[:-1]
        if self.p > HEX_THRESHOLD:
            result += f", ('{hex_string(self.G[0])}', '{hex_string(self.G[1])}')"
        else:
            result += f", ({self.G[0]}, {self.G[1]})"
        result += ")"
        return result


class Curve(CurveSubGroup):
    """Prime order subgroup of the points of an elliptic curve over Fp."""

    def __init__(
        self,
        p: Integer,
        a: Integer,
        b: Integer,
        G: Point,
        n: Integer,
        cofactor: int,
        weakness_check: bool = True,
        name: str | None = None,
    ) -> None:
        super().__init__(p, a, b, G)
        n = int_from_integer(n)

        # Security level is expressed in bits, where n-bit security
        # means that the attacker would have to perform 2^n operations
        # to break it. Security bits are half the key size for asymmetric
        # elliptic curve cryptography, i.e. half of the number of bits
        # required to express the group order n or, holding Hasse theorem,
        # to express the field prime p

        self.n = n
        self.nlen = n.bit_length()
        self.n_size = (self.nlen + 7) // 8

        # 5. Check that n is prime.
        if n < 2 or n % 2 == 0 or pow(2, n - 1, n) != 1:
            err_msg = "n is not prime: "
            err_msg += f"{hex_string(n)}" if n > HEX_THRESHOLD else f"{n}"
            raise BTClibValueError(err_msg)
        delta = int(2 * sqrt(self.p))
        # also check n with Hasse Theorem
        if cofactor < 2 and not self.p + 1 - delta <= n <= self.p + 1 + delta:
            err_msg = "n not in p+1-delta..p+1+delta: "
            err_msg += f"{hex_string(n)}" if n > HEX_THRESHOLD else f"{n}"
            raise BTClibValueError(err_msg)

        # 7. Check that G ≠ INF, nG = INF
        if self.G[1] == 0:
            err_msg = "INF point cannot be a generator"
            raise BTClibValueError(err_msg)
        jac_inf = _mult(n, self.GJ, self)
        if jac_inf[2] != 0:
            err_msg = "n is not the group order: "
            err_msg += f"{hex_string(n)}" if n > HEX_THRESHOLD else f"{n}"
            raise BTClibValueError(err_msg)

        # 6. Check cofactor
        exp_cofactor = int(1 / n + delta / n + self.p / n)
        if cofactor != exp_cofactor:
            err_msg = f"invalid cofactor: {cofactor}, expected {exp_cofactor}"
            raise BTClibValueError(err_msg)
        self.cofactor = cofactor

        # 8. Check that n ≠ p
        if n == p:
            raise BTClibValueError(
                f"n=p weak curve: {hex_string(n)}"
            )  # pragma: no cover

        if weakness_check:
            # 8. Check that p^i % n ≠ 1 for all 1≤i<100
            for i in range(1, 100):
                if pow(self.p, i, n) == 1:
                    raise UserWarning("weak curve")

        self.name = name

    def __str__(self) -> str:
        result = super().__str__()
        if self.n > HEX_THRESHOLD:
            result += f"\n n   = {hex_string(self.n)}"
        else:
            result += f"\n n   = {self.n}"
        result += f"\n cofactor = {self.cofactor}"
        return result

    def __repr__(self) -> str:
        result = super().__repr__()[:-1]
        if self.n > HEX_THRESHOLD:
            result += f", '{hex_string(self.n)}'"
        else:
            result += f", {self.n}"
        result += f", {self.cofactor}"
        result += ")"
        return result


datadir = path.join(path.dirname(__file__), "_data")

# Elliptic Curve Cryptography (ECC)
# Brainpool Standard Curves and Curve Generation
# https://tools.ietf.org/html/rfc5639
filename = path.join(datadir, "ec_Brainpool.json")
with open(filename, encoding="ascii") as file_:
    Brainpool_params2 = json.load(file_)
Brainpool: dict[str, Curve] = {
    ec_name: Curve(*Brainpool_params2[ec_name] + [True, ec_name])
    for ec_name in Brainpool_params2
}
# FIPS PUB 186-4
# FEDERAL INFORMATION PROCESSING STANDARDS PUBLICATION
# Digital Signature Standard (DSS)
# https://oag.ca.gov/sites/all/files/agweb/pdfs/erds1/fips_pub_07_2013.pdf
filename = path.join(datadir, "ec_NIST.json")
with open(filename, encoding="ascii") as file_:
    NIST_params2 = json.load(file_)
NIST: dict[str, Curve] = {
    ec_name: Curve(*NIST_params2[ec_name] + [True, ec_name]) for ec_name in NIST_params2
}
# SEC 2 v.1 curves, removed from SEC 2 v.2 as insecure ones
# http://www.secg.org/SEC2-Ver-1.0.pdf
filename = path.join(datadir, "ec_SEC2v1_insecure.json")
with open(filename, encoding="ascii") as file_:
    SEC2v1_params2 = json.load(file_)
SEC2v1: dict[str, Curve] = {
    ec_name: Curve(*SEC2v1_params2[ec_name] + [True, ec_name])
    for ec_name in SEC2v1_params2
}
# curves included in both SEC 2 v.1 and SEC 2 v.2
# http://www.secg.org/sec2-v2.pdf
filename = path.join(datadir, "ec_SEC2v2.json")
with open(filename, encoding="ascii") as file_:
    SEC2v2_params2 = json.load(file_)
SEC2v2: dict[str, Curve] = {}
for ec_name in SEC2v2_params2:
    SEC2v2[ec_name] = Curve(*SEC2v2_params2[ec_name] + [True, ec_name])
    SEC2v1[ec_name] = Curve(*SEC2v2_params2[ec_name] + [True, ec_name])

# with python>=3.9 use dictionary union operators
# CURVES = SEC2v1 | NIST | Brainpool
CURVES = SEC2v1
CURVES.update(NIST)
CURVES.update(Brainpool)

secp256k1 = CURVES["secp256k1"]


def mult(m_int: Integer, Q: Point | None = None, ec: Curve = secp256k1) -> Point:
    """Elliptic curve scalar multiplication."""
    m: int = int_from_integer(m_int) % ec.n

    if ec == secp256k1 and (Q is None or Q == ec.G) and libsecp256k1.is_available():
        return libsecp256k1.mult(m)

    if Q is None:
        QJ = ec.GJ
    else:
        ec.require_on_curve(Q)
        QJ = jac_from_aff(Q)

    R = _mult(m, QJ, ec)
    return ec.aff_from_jac(R)


def double_mult(
    u: Integer, H: Point, v: Integer, Q: Point, ec: Curve = secp256k1
) -> Point:
    """Double scalar multiplication (u*H + v*Q)."""
    ec.require_on_curve(H)
    HJ = jac_from_aff(H)

    ec.require_on_curve(Q)
    QJ = jac_from_aff(Q)

    u = int_from_integer(u) % ec.n
    v = int_from_integer(v) % ec.n
    R = _double_mult(u, HJ, v, QJ, ec)
    return ec.aff_from_jac(R)


def multi_mult(
    scalars: Sequence[Integer], points: Sequence[Point], ec: Curve = secp256k1
) -> Point:
    """Return the multi scalar multiplication u1*Q1 + ... + un*Qn.

    Use Bos-Coster's algorithm for efficient computation.
    """
    if len(scalars) != len(points):
        err_msg = "mismatch between number of scalars and points: "
        err_msg += f"{len(scalars)} vs {len(points)}"
        raise BTClibValueError(err_msg)

    ints = [int_from_integer(s) % ec.n for s in scalars]
    for Q in points:
        ec.require_on_curve(Q)
    jac_points = [jac_from_aff(Q) for Q in points]

    R = _multi_mult(ints, jac_points, ec)
    return ec.aff_from_jac(R)
