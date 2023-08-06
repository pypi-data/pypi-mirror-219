"""
Main entrypoint for fhzz.
"""

import argparse

import fhzz
import fhzz.campaign as campaign


def main():
    parser = argparse.ArgumentParser(
                 prog="fhzz",
                 description="Fuzz HTTP headers like a caveman")

    parser.add_argument("-V",
                        "--version",
                        action="store_true",
                        help="print package version")

    parser.add_argument("-w",
                        "--wordlist",
                        help="use a wordlist for fuzzing")

    parser.add_argument("-r",
                        "--request",
                        help="request whose headers to fuzz")

    parser.add_argument("-H",
                        "--header",
                        help="header to fuzz")

    parser.add_argument("-t",
                        "--target",
                        help="target to send fuzzed requests to")

    args = parser.parse_args()

    if args.version:
        print(f"fhzz {fhzz.__version__}")
    else:
        assert args.request, "Missing request argument!"
        assert args.target, "Missing target argument!"
        assert args.header, "Missing target argument!"
        campaign.start(args.request,
                       args.header,
                       args.target,
                       wordlist_path=args.wordlist)
