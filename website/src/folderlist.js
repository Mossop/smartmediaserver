// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/.

import React from "react";

const Folder = React.createClass({
  onClick(event) {
    this.props.selectFolder(this.props.folder);
  },

  render() {
    let className = "folder";
    if (this.props.selected == this.props.folder) {
      className += " selected";
    }

    return <li className={className}><span onClick={this.onClick} className="label">{this.props.folder.fields.name}</span><FolderContents {...this.props} folderKey={this.props.folder.pk}/></li>;
  }
});

const FolderContents = React.createClass({
  render() {
    let subfolders = this.props.folders.filter(f => f.fields.parent == this.props.folderKey);
    if (subfolders.length == 0) {
      return null;
    }

    return <ul>
      {subfolders.map((f) => <Folder key={f.pk} {...this.props} folder={f}/>)}
    </ul>;
  }
});

export default React.createClass({
  render() {
    let virtuals = this.props.virtualFolders.filter(f => f.fields.parent == null);
    let props = {
      selectFolder: this.props.onSelectFolder,
      selected: this.props.selectedFolder,
    };
    return <div className="folderlist">
      <ul onClick={this.onClick}>
        <li>
          All Photos
          <FolderContents {...props} folders={this.props.physicalFolders} folderKey={null}/>
        </li>
        {virtuals.map(f => <Folder key={f.pk} {...props} folders={this.props.virtualFolders} folder={f}/>)}
      </ul>
    </div>;
  }
});
