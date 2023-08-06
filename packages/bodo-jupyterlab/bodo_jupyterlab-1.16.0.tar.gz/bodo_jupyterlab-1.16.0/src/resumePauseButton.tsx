import React, { SyntheticEvent } from 'react';
import { pauseClusterHandler, resumeClusterHandler } from './handler';
import { ClusterStatus } from './types';
import { Tooltip } from 'react-tooltip';

type Props = {
  clusterStatus: ClusterStatus;
  uuid: string;
  startLoading: (status: string) => void;
  forceUpdate: () => void;
};

const ClusterResumePause = ({
  clusterStatus,
  uuid,
  startLoading,
  forceUpdate,
}: Props): JSX.Element | null => {
  const pauseCluster = (cluster_uuid: string) => async () => {
    if (
      !confirm(
        'Are you sure that you want to pause this cluster? Make sure not to pause clusters while the kernel is connecting.'
      )
    ) {
      return false;
    }
    await pauseClusterHandler(cluster_uuid);
    startLoading(ClusterStatus.PAUSING);
    forceUpdate();
  };

  const resumeCluster = (cluster_uuid: string) => async () => {
    if (!confirm('Are you sure that you want to resume this cluster')) {
      return false;
    }
    await resumeClusterHandler(cluster_uuid);
    startLoading(ClusterStatus.RESUMING);
    forceUpdate();
  };

  return (
    <>
      {[ClusterStatus.RUNNING, ClusterStatus.INITIALIZING].includes(clusterStatus) && (
        <div
          className="bodo-cluster-list-pause-unpause"
          data-tooltip-id="pause-cluster-tooltip"
          data-tooltip-content="Pause Cluster"
          onClick={pauseCluster(uuid)}
        >
          <svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 320 512">
            <path d="M48 64C21.5 64 0 85.5 0 112V400c0 26.5 21.5 48 48 48H80c26.5 0 48-21.5 48-48V112c0-26.5-21.5-48-48-48H48zm192 0c-26.5 0-48 21.5-48 48V400c0 26.5 21.5 48 48 48h32c26.5 0 48-21.5 48-48V112c0-26.5-21.5-48-48-48H240z" />
          </svg>
          <Tooltip id="pause-cluster-tooltip" />
        </div>
      )}

      {[ClusterStatus.PAUSED].includes(clusterStatus) && (
        <div
          className="bodo-cluster-list-pause-unpause"
          data-tooltip-id="resume-cluster-tooltip"
          data-tooltip-content="Resume Cluster"
          onClick={resumeCluster(uuid)}
        >
          <svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 384 512">
            <path d="M73 39c-14.8-9.1-33.4-9.4-48.5-.9S0 62.6 0 80V432c0 17.4 9.4 33.4 24.5 41.9s33.7 8.1 48.5-.9L361 297c14.3-8.7 23-24.2 23-41s-8.7-32.2-23-41L73 39z" />
          </svg>
          <Tooltip id="resume-cluster-tooltip" />
        </div>
      )}
    </>
  );
};

export default ClusterResumePause;
