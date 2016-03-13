// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/.

import React from "react";

const Folder = React.createClass({
  getInitialState() {
    return {
      open: true
    };
  },

  toggle() {
    this.setState({ open: !this.state.open });
  },

  onClick(event) {
    this.props.selectFolder(this.props.folder);
  },

  render() {
    let className = "folder";
    if (this.props.selected == this.props.folder) {
      className += " selected";
    }

    if (this.state.open) {
      return <li className={className}>
        <i className="fa fa-folder-open" onClick={this.toggle}></i>
        <span onClick={this.onClick} className="label">{this.props.folder.fields.name}</span>
        <FolderContents {...this.props} folderKey={this.props.folder.pk}/>
      </li>;
    } else {
      return <li className={className}>
        <i className="fa fa-folder" onClick={this.toggle}></i>
        <span onClick={this.onClick} className="label">{this.props.folder.fields.name}</span>
      </li>;
    }
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
    let fakeRoot = {
      folders: this.props.physicalFolders,
      folder: {
        pk: null,
        fields: {
          name: "All Photos"
        }
      },
    };

    let props = {
      selectFolder: this.props.onSelectFolder,
      selected: this.props.selectedFolder,
    };

    return <div className="folderlist">
      <ul onClick={this.onClick}>
        <Folder {...fakeRoot} {...props}/>
        {virtuals.map(f => <Folder key={f.pk} {...props} folders={this.props.virtualFolders} folder={f}/>)}
      </ul>
    </div>;
  }
});
