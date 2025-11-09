
import argparse
import requests

BASE_URL = "http://localhost:8000"  # change to your Pi's address if needed


def cmd_status(args):
    r = requests.get(f"{BASE_URL}/status/metrics", timeout=3)
    r.raise_for_status()
    data = r.json()
    print("=== STATUS ===")
    print("Mode:", data["mode"])
    print("State:", data["state"])
    print("Valve open:", data["valve_open"])
    if data["air"]:
        print(
            "Air:",
            f"{data['air']['temperature_c']:.1f} °C,",
            f"{data['air']['humidity_rel']:.1f} %",
        )
    if data["soil"]:
        print(
            "Soil:",
            f"{data['soil']['temperature_c']:.1f} °C,",
            f"{data['soil']['moisture_rel']*100:.1f} %",
        )


def cmd_valve(args):
    payload = {"action": args.action}
    if args.seconds:
        payload["seconds"] = args.seconds
    r = requests.post(f"{BASE_URL}/control/valve", json=payload, timeout=3)
    r.raise_for_status()
    print("OK:", r.json())


def cmd_mode(args):
    r = requests.post(
        f"{BASE_URL}/control/mode",
        json={"mode": args.mode},
        timeout=3,
    )
    r.raise_for_status()
    print("OK:", r.json())


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    p_status = sub.add_parser("status", help="show current metrics")
    p_status.set_defaults(func=cmd_status)

    p_valve = sub.add_parser("valve", help="open/close valve")
    p_valve.add_argument("action", choices=["open", "close"])
    p_valve.add_argument("--seconds", type=int, default=None)
    p_valve.set_defaults(func=cmd_valve)

    p_mode = sub.add_parser("mode", help="set mode (auto/manual)")
    p_mode.add_argument("mode", choices=["auto", "manual"])
    p_mode.set_defaults(func=cmd_mode)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
