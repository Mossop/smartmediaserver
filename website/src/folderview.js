// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/.

import React from "react";

import GridTile from 'material-ui/lib/grid-list/grid-tile';
import FontIcon from 'material-ui/lib/font-icon';

const PhotoThumbnail = React.createClass({
  onClick() {
    this.props.selectPhoto(this.props.photo);
  },

  render() {
    return <div className="viewtile photo" onClick={this.onClick}>
      <GridTile title={this.props.photo.fields.name}>
        <div className="viewtilecontent">
          <img src={`/photo/${this.props.photo.pk}/thumbnail/200`}/>
        </div>
      </GridTile>
    </div>;
  }
});

const FolderThumbnail = React.createClass({
  onClick() {
    this.props.selectFolder(this.props.folder);
  },

  render() {
    return <div className="viewtile folder" onClick={this.onClick}>
      <GridTile title={this.props.folder.fields.name}>
        <div className="viewtilecontent">
          <FontIcon className="material-icons" style={{ fontSize: 96 }}>{this.props.children}</FontIcon>
        </div>
      </GridTile>
    </div>;
  }
});

export default React.createClass({
  render() {
    let parent = this.props.hierarchy.folders.get(this.props.folder.fields.parent)
    if (!parent && this.props.folder != this.props.hierarchy.root) {
      parent = this.props.hierarchy.root;
    }
    let subfolders = Array.from(this.props.hierarchy.folders.values()).filter(f => f.fields.parent == this.props.folder.pk);
    let photos = this.props.folder.photos ?
                 this.props.folder.photos.map(pk => this.props.photos.get(pk)) :
                 [];

    return <div className="folderview">
      {parent ? <FolderThumbnail key={`folder-${parent.pk}`} folder={parent} selectFolder={this.props.selectFolder}>arrow_back</FolderThumbnail> : ""}
      {subfolders.map((f) => <FolderThumbnail key={`folder-${f.pk}`} folder={f} selectFolder={this.props.selectFolder}>folder</FolderThumbnail>)}
      {photos.map((p) => <PhotoThumbnail key={`photo-${p.pk}`} photo={p} selectPhoto={this.props.selectPhoto} />)}
    </div>;
  }
});
