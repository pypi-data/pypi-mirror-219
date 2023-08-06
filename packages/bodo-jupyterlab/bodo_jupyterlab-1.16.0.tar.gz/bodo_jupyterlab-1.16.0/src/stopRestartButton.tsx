import React from 'react';
import { Tooltip } from 'react-tooltip';
import { restartClusterHandler, stopClusterHandler } from './handler';
import { ClusterStatus } from './types';

type Props = {
  clusterStatus: ClusterStatus;
  uuid: string;
  startLoading: (status: string) => void;
  forceUpdate: () => void;
};

const ClusterStopRestart = ({
  clusterStatus,
  uuid,
  startLoading,
  forceUpdate,
}: Props): JSX.Element | null => {
  const stopCluster = (cluster_uuid: string) => async () => {
    if (!confirm('Are you sure that you want to stop this cluster?')) {
      return false;
    }

    startLoading(ClusterStatus.STOPPING);
    await stopClusterHandler(cluster_uuid);
    forceUpdate();
  };

  const restartCluster = (cluster_uuid: string) => async () => {
    if (!confirm('Are you sure that you want to restart this cluster')) {
      return false;
    }

    startLoading(ClusterStatus.INPROGRESS);
    await restartClusterHandler(cluster_uuid);
    forceUpdate();
  };

  return (
    <>
      {[ClusterStatus.RUNNING, ClusterStatus.PAUSED, ClusterStatus.INITIALIZING].includes(
        clusterStatus
      ) && (
        <div>
          <div
            className="bodo-cluster-list-stop-restart"
            data-tooltip-id="stop-cluster-tooltip"
            data-tooltip-content="Stop Cluster"
            onClick={stopCluster(uuid)}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              height="1em"
              viewBox="0 0 384 512"
              id="stop-svg"
            >
              <path d="M0 128C0 92.7 28.7 64 64 64H320c35.3 0 64 28.7 64 64V384c0 35.3-28.7 64-64 64H64c-35.3 0-64-28.7-64-64V128z" />
            </svg>
            <Tooltip id="stop-cluster-tooltip" />
          </div>
        </div>
      )}

      {[ClusterStatus.STOPPED].includes(clusterStatus) && (
        <div
          className="bodo-cluster-list-stop-restart"
          data-tooltip-id="restart-cluster-tooltip"
          data-tooltip-content="Restart Cluster"
          onClick={restartCluster(uuid)}
        >
          <svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512">
            <path d="M463.5 224H472c13.3 0 24-10.7 24-24V72c0-9.7-5.8-18.5-14.8-22.2s-19.3-1.7-26.2 5.2L413.4 96.6c-87.6-86.5-228.7-86.2-315.8 1c-87.5 87.5-87.5 229.3 0 316.8s229.3 87.5 316.8 0c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0c-62.5 62.5-163.8 62.5-226.3 0s-62.5-163.8 0-226.3c62.2-62.2 162.7-62.5 225.3-1L327 183c-6.9 6.9-8.9 17.2-5.2 26.2s12.5 14.8 22.2 14.8H463.5z" />
          </svg>
          <Tooltip id="restart-cluster-tooltip" />
        </div>
      )}
    </>
  );
};

export default ClusterStopRestart;
