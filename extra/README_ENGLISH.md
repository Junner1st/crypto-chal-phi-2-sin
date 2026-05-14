# Phi2Sin (Φ to Signature)

## Files

- `field.py`: finite-field helpers
- `curve.py`: elliptic-curve group and the public automorphism
- `relation.py`: constraint-friendly map-to-curve relation
- `scheme.py`: toy relation-based signature scheme
- `service.py`: command dispatcher

## Challenge Design

The relation is not a true hash-to-curve map. On the $j = 0$ curve

$$
y^2 = x^3 - 17
$$

the map

$$
\phi(x, y) = (\omega x, y)
$$

is a curve automorphism. Since scalar multiplication commutes with this map,

$$
\phi(sk \cdot P) = sk \cdot \phi(P)
$$

a signature on one relation point can be transported to a signature on another.

The signing oracle refuses to sign the reserved account directly, but the public
automorphism lets us find a different valid relation point whose image lands on
the reserved account's relation point.

## Exploit Process

1. Request `params` to get `p`, `b`, `window`, `item_limit`, `account_id`, and the automorphism coefficient `a`.
2. Iterate over candidate reserved-account indices `k2` and set `x2 = account_id * window + k2`.
3. Check that `x2` gives a valid curve point and that the witness `z` satisfies the relation constraints.
4. Pull the point back through the inverse automorphism with `x1 = a^-1 * x2`.
5. Convert `x1` into `(m1, k1)` and ensure `m1` is not the reserved account.
6. Ask the oracle to sign the non-reserved relation point `(x1, y)`.
7. Push the returned token forward with the automorphism, giving `(a*sx, sy)`.
8. Submit the transported token for the reserved account point `(x2, y)` to get the flag.

[solver script is here](solve.py)

## FLAG

`CCCTF{Ya_wen2__faahhh___}`
