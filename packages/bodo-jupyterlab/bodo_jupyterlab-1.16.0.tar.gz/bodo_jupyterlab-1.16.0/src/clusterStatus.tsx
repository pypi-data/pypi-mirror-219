import React from 'react';

type StatusProps = {
  status: string;
};

const ClusterStatusComponent = ({ status }: StatusProps) => {
  return <div className={`cluster-status ${status.toLowerCase()}`}>{status}</div>;
};

export default ClusterStatusComponent;
