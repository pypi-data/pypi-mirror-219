# Built-in Imports
import argparse

from chimerapy.engine import _logger

logger = _logger.getLogger("chimerapy-engine")


def main():

    # Internal Imports
    from chimerapy.engine.worker import Worker

    # Create the arguments for Worker CI
    parser = argparse.ArgumentParser(description="ChimeraPy-Engine Worker CI")

    # Adding the arguments
    parser.add_argument("--name", type=str, help="Name of the Worker", required=True)
    parser.add_argument(
        "--zeroconf", type=bool, help="Use Zeroconf to find Manager", default=False
    )
    parser.add_argument("--ip", type=str, help="Manager's IP Address", default="")
    parser.add_argument("--port", type=int, help="Manager's Port", default=-1)
    parser.add_argument("--id", type=str, help="ID of the Worker", default=None)
    parser.add_argument("--wport", type=int, help="Worker's Port", default=0)
    parser.add_argument(
        "--delete",
        type=bool,
        help="Delete Worker's data after transfer to Manager's computer",
        default=True,
    )

    args = parser.parse_args()

    # Convert the Namespace to a dictionary
    d_args = vars(args)

    # Create Worker and execute connect
    worker = Worker(
        name=d_args["name"],
        delete_temp=d_args["delete"],
        id=d_args["id"],
        port=d_args["wport"],
    )
    if d_args["zeroconf"]:
        worker.connect(method="zeroconf")
    else:

        # Check inputs
        if d_args["ip"] == "" or d_args["port"] == -1:
            worker.shutdown()
            raise argparse.ArgumentError(
                "When not using Zeroconf, an ``ip`` and ``port`` are needed"
            )

        worker.connect(method="ip", host=d_args["ip"], port=d_args["port"])

    # Wait until told to shutdown
    worker.idle()
    worker.shutdown()


if __name__ == "__main__":
    main()
