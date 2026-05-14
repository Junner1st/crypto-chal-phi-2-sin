import json
from pwn import context, remote


HOST = "127.0.0.1"
PORT = 1340

context.log_level = "error"

def is_square(x: int, p: int) -> bool:
    x %= p
    if x == 0:
        return True
    return pow(x, (p - 1) // 2, p) == 1


def sqrt_mod(x: int, p: int) -> int:
    r = pow(x % p, (p + 1) // 4, p)
    assert (r * r) % p == x % p
    return r


def find_quadratic_y(rhs: int, p: int) -> tuple[int, int] | None:
    if not is_square(rhs, p):
        return None

    y = sqrt_mod(rhs, p)
    if not is_square(y, p):
        y = (-y) % p

    if not is_square(y, p):
        return None

    z = sqrt_mod(y, p)
    return y, z


class Client:
    def __init__(self, host: str, port: int):
        self.io = remote(host, port)
        self.io.recvuntil(b"> ")

    def close(self) -> None:
        self.io.sendline(b"exit")
        self.io.close()

    def call(self, cmd: str, payload: dict | None = None) -> dict:
        if payload is None:
            line = cmd
        else:
            line = f"{cmd} {json.dumps(payload, separators=(',', ':'))}"

        self.io.sendline(line.encode())
        data = self.io.recvuntil(b"> ", drop=True).strip()
        return json.loads(data.splitlines()[-1])


def main() -> None:
    client = Client(HOST, PORT)

    try:
        params = client.call("params")
        assert params["ok"], params

        p = params["p"]
        b = params["b"]
        window = params["window"]
        item_limit = params["item_limit"]
        account_id = params["account_id"]
        a = params["a"]
        a_inv = pow(a, 2, p)

        for k2 in range(window):
            x2 = account_id * window + k2
            rhs = (pow(x2, 3, p) + b) % p

            yz = find_quadratic_y(rhs, p)
            if yz is None:
                continue

            y, z = yz
            x1 = (a_inv * x2) % p

            if x1 >= item_limit * window:
                continue

            m1, k1 = divmod(x1, window)
            if m1 == account_id:
                continue

            sign_resp = client.call(
                "sign",
                {
                    "m": m1,
                    "x": x1,
                    "y": y,
                    "k": k1,
                    "z": z,
                },
            )
            if not sign_resp.get("ok"):
                continue

            token = sign_resp["token"]
            token2 = {
                "x": (a * token["x"]) % p,
                "y": token["y"],
            }

            verify_resp = client.call(
                "verify",
                {
                    "x": x2,
                    "y": y,
                    "k": k2,
                    "z": z,
                    "sx": token2["x"],
                    "sy": token2["y"],
                },
            )

            if verify_resp.get("ok"):
                print("found k =", k2)
                print("signed m =", m1)
                print("signed k =", k1)
                print("flag =", verify_resp["flag"])
                return

        raise RuntimeError("attack failed; parameters may have been changed")
    finally:
        client.close()


if __name__ == "__main__":
    main()
