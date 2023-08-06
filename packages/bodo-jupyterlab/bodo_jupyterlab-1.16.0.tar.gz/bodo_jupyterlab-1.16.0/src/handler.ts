import { URLExt } from '@jupyterlab/coreutils';

import { ServerConnection } from '@jupyterlab/services';

import { LRUCache } from 'typescript-lru-cache';
import { IConfig } from './types';

/**
 * Call the API extension
 *
 * @param path The API endpoint
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI<T>(path = '', init: RequestInit = {}): Promise<T> {
  // Make request to Jupyter API
  const settings = ServerConnection.makeSettings();
  const requestUrl = URLExt.join(settings.baseUrl, path);
  console.debug('handler.ts:requestAPI:requestUrl: ', requestUrl);

  let response: Response;
  try {
    response = await ServerConnection.makeRequest(requestUrl, init, settings);
  } catch (error: any) {
    console.error('handler.ts:requestAPI:error: ', error);
    throw new ServerConnection.NetworkError(error);
  }

  const data = await response.json();
  console.debug('handler.ts:requestAPI:data: ', data);

  if (!response.ok) {
    throw new ServerConnection.ResponseError(response, data.message);
  }

  return data;
}

export async function createRemoteIKernelHandler(clusterUUID: string): Promise<any> {
  const data: { remote_kernel_name: string; e: any } = await requestAPI<any>(
    `cluster-remote-ikernel/${clusterUUID}`,
    { method: 'POST' }
  );
  if (data.e) {
    throw new Error(data.e);
  }
  return data.remote_kernel_name;
}

export async function getClusterListHandler(): Promise<any> {
  const data: { clusters: any[]; e: any } = await requestAPI<any>(
    `bodo/cluster?forceRefresh=False`,
    {
      method: 'GET',
    }
  );
  if (data.e) {
    throw new Error(data.e);
  }
  return data.clusters;
}

export async function resumeClusterHandler(clusterUUID: string): Promise<any> {
  try {
    await requestAPI<any>(`bodo/cluster/${clusterUUID}/resume`, {
      method: 'Put',
    });
  } catch (error: any) {
    throw new Error(error);
  }
}

export async function pauseClusterHandler(clusterUUID: string): Promise<any> {
  try {
    await requestAPI<any>(`bodo/cluster/${clusterUUID}/pause`, {
      method: 'Put',
    });
  } catch (error: any) {
    throw new Error(error);
  }
}

export async function stopClusterHandler(clusterUUID: string): Promise<any> {
  try {
    await requestAPI<any>(`bodo/cluster/${clusterUUID}/stop`, {
      method: 'Put',
    });
  } catch (e: any) {
    throw new Error(e);
  }
}

export async function restartClusterHandler(clusterUUID: string): Promise<any> {
  try {
    await requestAPI<any>(`bodo/cluster/${clusterUUID}/restart`, {
      method: 'Put',
    });
  } catch (e: any) {
    throw new Error(e);
  }
}

export async function refreshClusterListHandler(): Promise<any> {
  // Utilizes the same endpoint as Cluster List Handler however with
  // forceRefresh parameter set to true
  const data: { clusters: any[]; e: any } = await requestAPI<any>(
    `bodo/cluster?forceRefresh=True`,
    {
      method: 'GET',
    }
  );
  if (data.e) {
    throw new Error(data.e);
  }
  return data.clusters;
}

export async function refreshCatalogListHandler(): Promise<any> {
  const data: { catalogs: any[]; e: any } = await requestAPI<any>(
    `bodo/catalog?forceRefresh=True`,
    {
      method: 'GET',
    }
  );
  if (data.e) {
    throw new Error(data.e);
  }
  return data.catalogs;
}

const cache = new LRUCache<string, IConfig>({ maxSize: 1 });
export async function fetchConfig(): Promise<IConfig> {
  const cacheData = cache.get('data');
  if (cacheData) {
    return Promise.resolve(cacheData);
  }

  const data: IConfig = await requestAPI<any>('bodo/config', {
    method: 'GET',
  });
  if (data.e) {
    throw new Error(data.e);
  }

  cache.set('data', data);
  return data;
}
