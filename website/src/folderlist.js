// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/.

import React from "react";

const Folder = React.createClass({
  render() {
    return <li>{this.props.folder.fields.name}<FolderContents folders={this.props.folders} folderKey={this.props.folder.pk}/></li>;
  }
});

const FolderContents = React.createClass({
  render() {
    let subfolders = this.props.folders.filter(f => f.fields.parent == this.props.folderKey);
    if (subfolders.length == 0) {
      return null;
    }
    return <ul>
      {subfolders.map((f) => <Folder key={f.pk} folders={this.props.folders} folder={f}/>)}
    </ul>;
  }
});

export default React.createClass({
  render() {
    let virtuals = this.props.virtualFolders.filter(f => f.fields.parent == null);
    return <div className="folderlist">
      <ul>
        <li>
          All Photos
          <FolderContents folders={this.props.physicalFolders} folderKey={null}/>
        </li>
        {virtuals.map(f => <Folder key={f.pk} folders={this.props.virtualFolders} folder={f}/>)}
      </ul>
    </div>;
  }
});
