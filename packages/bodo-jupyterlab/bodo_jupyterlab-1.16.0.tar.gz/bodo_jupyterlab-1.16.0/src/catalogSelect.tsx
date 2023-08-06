/* This file provides the cache of catalogs which the user can select
 * a catalog from, and uses the selected catalog (if any) to set notebook metadata
 * toolbar. It refreshes the list of available catalogs periodically. It is used in
 * ./toolbar.tsx.
 * */

import { NotebookPanel } from '@jupyterlab/notebook';
import { useQuery } from '@tanstack/react-query';
import React, { useEffect, useState } from 'react';
import { refreshCatalogListHandler } from './handler';

interface IProps {
  panel: NotebookPanel;
}

export const CatalogsSelect: React.FC<IProps> = ({ panel }) => {
  const getCatalogs = async () => {
    try {
      return refreshCatalogListHandler();
    } catch (err) {
      console.error('Error fetching catalogs', err);
      return [];
    }
  };

  const { data: catalogs } = useQuery(['catalogs'], () => getCatalogs(), {
    // If set to a number, continuously refetch at this frequency in ms
    refetchInterval: 60000,
  });
  const [isDisabled, setIsDisabled] = useState(true);
  const [catalog, setCatalog] = useState<any>(undefined);

  useEffect(() => {
    panel.context.ready.then(() => {
      setIsDisabled(false);
      setCatalog(panel.model?.metadata.get('bodo-catalog'));
    });
  }, []);

  const handleChange = (e: any) => {
    panel.model?.metadata.set('bodo-catalog', e.target.value);

    // Update connection metadata for all cells
    const numCells = panel?.model?.cells.length ?? 0;

    for (let i = 0; i < numCells; i++) {
      const cell = panel?.model?.cells.get(i);

      cell?.metadata.set('bodo-catalog', e.target.value);
    }

    setCatalog(e.target.value);
  };

  return (
    <div className="jp-HTMLSelect jp-DefaultStyle">
      <select
        style={{
          marginInline: '5px',
          color: 'black',
        }}
        disabled={isDisabled}
        onChange={handleChange}
        value={catalog}
        placeholder="Select catalog"
      >
        <option value="" selected={!catalog}>
          Select Catalog
        </option>
        {catalogs?.map((c: any) => (
          <option value={JSON.stringify(c)}>{c.name}</option>
        ))}
      </select>
      <span className="f1ozlkqi">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          viewBox="0 0 18 18"
          data-icon="ui-components:caret-down-empty"
        >
          <g
            xmlns="http://www.w3.org/2000/svg"
            className="jp-icon3"
            fill="#616161"
            shapeRendering="geometricPrecision"
          >
            <path d="M5.2,5.9L9,9.7l3.8-3.8l1.2,1.2l-4.9,5l-4.9-5L5.2,5.9z"></path>
          </g>
        </svg>
      </span>
    </div>
  );
};
