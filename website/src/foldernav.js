// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/.

import React from "react";

import LeftNav from 'material-ui/lib/left-nav';
import MenuItem from 'material-ui/lib/menus/menu-item';
import FontIcon from 'material-ui/lib/font-icon';

const FolderItem = React.createClass({
  onClick(event) {
    this.props.selectFolder(this.props.folder);
  },

  render() {
    return <MenuItem leftIcon={<FontIcon className="material-icons">folder</FontIcon>} onTouchTap={this.onClick}>{this.props.folder.fields.name}</MenuItem>;
  }
});

export default React.createClass({
  render() {
    return <LeftNav docked={false} open={this.props.open} onRequestChange={this.props.toggleNav}>
      {this.props.hierarchies.map((h, i) => <FolderItem key={i} folder={h.root} selectFolder={this.props.selectFolder} />)}
    </LeftNav>;
  }
});
