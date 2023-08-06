/* This file creates custom cell header dropdowns to select cell language and sets cell metadata for code cells to
 * set the catalog for native sql queries when a (snowflake) sql catalog is selected. The languages available currently
 * are : Parallel_python (default) , python and sql.
 * */

import { JupyterFrontEndPlugin, JupyterFrontEnd } from '@jupyterlab/application';
import { NotebookPanel, StaticNotebook } from '@jupyterlab/notebook';
import { IEditorServices } from '@jupyterlab/codeeditor';
import { ICellHeader, CellHeader, CodeCell, MarkdownCell, RawCell, Cell } from '@jupyterlab/cells';
import { ReactWidget, UseSignal } from '@jupyterlab/apputils';
import React from 'react';
import { Signal } from '@lumino/signaling';
import { SupportedLanguages } from './types';
import { ReadonlyPartialJSONValue } from '@lumino/coreutils';
import { fetchConfig } from './handler';

// Create the plugin to override the default IContentFactory
export const cellFactory: JupyterFrontEndPlugin<NotebookPanel.IContentFactory> = {
  id: 'jupyterlab-codecellselect:factory',
  provides: NotebookPanel.IContentFactory,
  requires: [IEditorServices],
  autoStart: true,
  activate: (app: JupyterFrontEnd, editorServices: IEditorServices) => {
    const editorFactory = editorServices.factoryService.newInlineEditor;
    return new ContentFactoryWithSelect({ editorFactory });
  },
};

// Custom ContentFactory that overrides functions that create the elements
// we need to modify
export class ContentFactoryWithSelect extends NotebookPanel.ContentFactory {
  // Variable indicating whether the header should be rendered on the current cell.
  private _RENDER_HEADER: boolean | null;
  // Feature flag to check whether catalogs are enabled
  private _CATALOG_MODE: boolean | null;

  constructor(props: Cell.ContentFactory.IOptions | undefined) {
    super(props);
    this._RENDER_HEADER = null;
    this._CATALOG_MODE = null;
    // set the feature flag from the configuration which picks up the value from the backend.
    this._setCatalogMode();
  }

  get RENDER_HEADER(): boolean | null {
    return this._RENDER_HEADER;
  }

  set RENDER_HEADER(value: boolean | null) {
    this._RENDER_HEADER = value;
  }

  async _setCatalogMode(): Promise<void> {
    let catalogmode = this._CATALOG_MODE;
    if (catalogmode === null) {
      catalogmode = (await fetchConfig()).catalog_mode;
    }
    this._CATALOG_MODE = catalogmode;
  }

  createCellHeader(): ICellHeader {
    if (this.RENDER_HEADER) {
      return new CellHeaderWithSelect(this._CATALOG_MODE);
    }

    return new CellHeader();
  }

  createCodeCell(options: CodeCell.IOptions, parent: StaticNotebook): CodeCell {
    this.RENDER_HEADER = true;
    return new PythonSQLCodeCell(options, parent.model?.metadata.get('bodo-catalog'));
  }

  createMarkdownCell(options: MarkdownCell.IOptions, parent: StaticNotebook): MarkdownCell {
    // don't render the language selector on markdown cells even if catalog mode is enabled
    this.RENDER_HEADER = false;
    return super.createMarkdownCell(options, parent);
  }

  createRawCell(options: RawCell.IOptions, parent: StaticNotebook): RawCell {
    // don't render the language selector on raw cells even if catalog mode is enabled
    this.RENDER_HEADER = false;
    return super.createRawCell(options, parent);
  }
}

export class PythonSQLCodeCell extends CodeCell {
  constructor(options: CodeCell.IOptions, catalog?: ReadonlyPartialJSONValue) {
    super(options);
    this.setMimeType = this.setMimeType.bind(this);

    const cellHeader = this.getCellHeader();
    if (cellHeader) {
      // Attach callbacks to header signals
      cellHeader.getLangChanged().connect(this.setLangMetadata, this);

      // If the cell already has language metadata set the cell header to the
      // correct selection or default to Parallel Python
      const lang = this.model.metadata.get('lang') || SupportedLanguages.PARALLEL_PYTHON;
      cellHeader.setLang(lang as SupportedLanguages);

      this.ready.then(() => this.setMimeType(this.getMimeTypeFromLang(lang as SupportedLanguages)));
    }

    this.ready.then(() => this.model.metadata.set('bodo-catalog', catalog));
  }

  outputFooterNode: HTMLDivElement | null = null;

  private getMimeTypeFromLang(lang: SupportedLanguages): string {
    if (lang === SupportedLanguages.SQL) {
      // SQL highlighting for SQL cells
      return `text/x-sql`;
    } else {
      // Fall back to Python for everything else,
      // including Parallel Python which has the
      // same syntax as Python.
      return `text/x-python`;
    }
  }

  private setLangMetadata(emitter: CellHeaderWithSelect, lang: SupportedLanguages) {
    this.model.metadata.set('lang', lang);
    this.setMimeType(this.getMimeTypeFromLang(lang));
  }

  private setOutputMetadata(emitter: CellHeaderWithSelect, output: string) {
    this.model.metadata.set('output', output);
  }

  /**
   * Sets the mimetype of the current cell's contents. Helpful for syntax highlighting.
   * A mime-type dictates what sort of type a file confirms to. In this case, it refers to the type of the cell contents.
   * It is similar to a file extension. Jupyter uses mime-type for cell syntax highlighting. For example, `text/x-python`
   * tells Jupyter to use python syntax highlighting and in case of `text/sql` it shows syntax highlighting for sql.
   * @param mimeType string
   */
  private setMimeType(mimeType: string): void {
    this.editorWidget.model.mimeType = mimeType;
  }

  private getCellHeader(): CellHeaderWithSelect | null {
    let cellHeader: CellHeaderWithSelect | null = null;
    const children = this.children();
    for (let child = children.next(); child; child = children.next()) {
      if (child.hasClass('jp-Cell-header')) {
        cellHeader = child as CellHeaderWithSelect;
        break;
      }
    }

    return cellHeader;
  }
}

export class CellHeaderWithSelect extends ReactWidget implements ICellHeader {
  private _langChanged = new Signal<CellHeaderWithSelect, SupportedLanguages>(this);
  private _isSelectingSignal = new Signal<CellHeaderWithSelect, boolean>(this);

  _lang = SupportedLanguages.PARALLEL_PYTHON;
  _output = '';

  private _isSelecting = false;
  private catalogMode: boolean | null = false;

  constructor(catalogMode: boolean | null = false) {
    super();

    this.handleToggle = this.handleToggle.bind(this);
    this.setLangParallelPython = this.setLangParallelPython.bind(this);
    this.setLangPython = this.setLangPython.bind(this);
    this.setLangSQL = this.setLangSQL.bind(this);
    this.setLang = this.setLang.bind(this);
    this.catalogMode = catalogMode;
  }

  handleToggle(): void {
    this._isSelecting = !this._isSelecting;
    this._isSelectingSignal.emit(this._isSelecting);
  }

  setLangParallelPython(): void {
    this._lang = SupportedLanguages.PARALLEL_PYTHON;
    this._langChanged.emit(this._lang);
    this.handleToggle();
  }

  setLangPython(): void {
    this._lang = SupportedLanguages.PYTHON;
    this._langChanged.emit(this._lang);
    this.handleToggle();
  }

  setLangSQL(): void {
    this._lang = SupportedLanguages.SQL;
    this._langChanged.emit(this._lang);
    this.handleToggle();
  }

  setLang(lang: SupportedLanguages): void {
    this._lang = lang;
    this._langChanged.emit(lang);
  }

  public getLangChanged(): Signal<CellHeaderWithSelect, SupportedLanguages> {
    return this._langChanged;
  }

  render() {
    return (
      <select
        style={{
          border: 'none',
          background: '#A0B2DB', //'var(--jp-cell-editor-background)',
          color: 'black',
          position: 'absolute',
          height: '17px',
          fontSize: '12px',
          zIndex: 998,
          right: '0px',
          top: '-17px',
        }}
        onChange={(e) => {
          this._lang = e.target.value as SupportedLanguages;
          this._langChanged.emit(this._lang);
          this.handleToggle();
        }}
      >
        <UseSignal signal={this._langChanged} initialArgs={this._lang}>
          {(_, lang) => (
            <>
              <option
                value={SupportedLanguages.PARALLEL_PYTHON}
                selected={SupportedLanguages.PARALLEL_PYTHON === lang}
              >
                Parallel-Python
              </option>
              {this.catalogMode ? (
                <option value={SupportedLanguages.SQL} selected={SupportedLanguages.SQL === lang}>
                  SQL
                </option>
              ) : null}
              <option
                value={SupportedLanguages.PYTHON}
                selected={SupportedLanguages.PYTHON === lang}
              >
                Python
              </option>
            </>
          )}
        </UseSignal>
      </select>
    );
  }
}
