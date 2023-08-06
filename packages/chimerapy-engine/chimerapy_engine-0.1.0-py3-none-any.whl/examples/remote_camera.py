from typing import Dict
import time
import pathlib
import os

import cv2

import chimerapy.engine as cpe

CWD = pathlib.Path(os.path.abspath(__file__)).parent
cpe.debug()


class WebcamNode(cpe.Node):
    def setup(self):
        self.vid = cv2.VideoCapture(0)

    def step(self) -> cpe.DataChunk:
        time.sleep(1 / 30)
        ret, frame = self.vid.read()
        self.save_video(name="test", data=frame, fps=15)
        data_chunk = cpe.DataChunk()
        data_chunk.add("frame", frame, "image")
        return data_chunk

    def teardown(self):
        self.vid.release()


class ShowWindow(cpe.Node):
    def step(self, data_chunks: Dict[str, cpe.DataChunk]):

        for name, data_chunk in data_chunks.items():
            self.logger.debug(f"{self}: got from {name}, data={data_chunk}")

            cv2.imshow(name, data_chunk.get("frame")["value"])
            cv2.waitKey(1)


class RemoteCameraGraph(cpe.Graph):
    def __init__(self):
        super().__init__()
        self.web = WebcamNode(name="web")
        self.show = ShowWindow(name="show")

        self.add_nodes_from([self.web, self.show])
        self.add_edge(src=self.web, dst=self.show)
        self.node_ids = [self.web.id, self.show.id]


if __name__ == "__main__":

    # Create default manager and desired graph
    manager = cpe.Manager(logdir=CWD / "runs")
    graph = RemoteCameraGraph()
    worker = cpe.Worker(name="local", id="local")

    # Then register graph to Manager
    worker.connect(host=manager.host, port=manager.port)

    # Wait until workers connect
    while True:
        q = input("All workers connected? (Y/n)")
        if q.lower() == "y":
            break

    # Assuming one worker
    # mapping = {"remote": [graph.web.id], worker.id: [graph.show.id]}
    mapping = {worker.id: graph.node_ids}

    # Commit the graph
    manager.commit_graph(graph=graph, mapping=mapping).result(timeout=60)
    manager.start().result(timeout=5)

    # Wail until user stops
    while True:
        q = input("Ready to start? (Y/n)")
        if q.lower() == "y":
            break

    manager.record().result(timeout=5)

    # Wail until user stops
    while True:
        q = input("Stop? (Y/n)")
        if q.lower() == "y":
            break

    manager.stop().result(timeout=5)
    manager.collect().result()
    manager.shutdown()
