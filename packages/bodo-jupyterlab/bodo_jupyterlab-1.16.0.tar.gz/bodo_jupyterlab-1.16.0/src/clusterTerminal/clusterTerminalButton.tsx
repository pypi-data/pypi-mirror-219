import { JupyterFrontEnd } from '@jupyterlab/application';
import React from 'react';
import { ClusterStatus, ICluster } from '../types';
import { Tooltip } from 'react-tooltip';

type Props = {
  cluster: ICluster;
  app: JupyterFrontEnd;
};

// Component to display button to create terminal connected to cluster if cluster is running
// and nothing if the cluster is not running
const ClusterTerminalButton = ({ app, cluster }: Props) => {
  const createTerminal = () => {
    app.commands.execute('terminal:create-new', { cluster: JSON.stringify(cluster) });
  };

  return (
    <>
      {[ClusterStatus.RUNNING, ClusterStatus.INITIALIZING].includes(cluster.status) ? (
        <div
          className="bodo-cluster-list-terminal"
          onClick={createTerminal}
          data-tooltip-id="terminal-tooltip"
          data-tooltip-content="Open Terminal"
        >
          <svg xmlns="http://www.w3.org/2000/svg" height="24" width="24" version="1.1">
            <g transform="translate(0 -1028.4)">
              <path
                d="m3 1030.4c-1.1046 0-2 0.9-2 2v7 2 7c0 1.1 0.8954 2 2 2h9 9c1.105 0 2-0.9 2-2v-7-2-7c0-1.1-0.895-2-2-2h-9-9z"
                fill="#2c3e50"
              />
              <path
                d="m3 2c-1.1046 0-2 0.8954-2 2v3 3 1 1 1 3 3c0 1.105 0.8954 2 2 2h9 9c1.105 0 2-0.895 2-2v-3-4-2-3-3c0-1.1046-0.895-2-2-2h-9-9z"
                transform="translate(0 1028.4)"
                fill="#34495e"
              />
              <path
                d="m4 5.125v1.125l3 1.75-3 1.75v1.125l5-2.875-5-2.875zm5 4.875v1h5v-1h-5z"
                transform="translate(0 1028.4)"
                fill="#1db100"
              />
            </g>
          </svg>
          <Tooltip id="terminal-tooltip" />
        </div>
      ) : null}
    </>
  );
};

export default ClusterTerminalButton;
