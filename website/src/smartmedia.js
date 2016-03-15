// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/.
"use strict";

async function fetchJSON(url) {
  let response = await fetch(url);
  if (!response.ok) {
    throw new Error(response.statusText);
  }

  return await response.json();
}

class DjangoObject {
  constructor(json) {
    if (!json) {
      return;
    }
    this.id = json.pk;
    for (let name in json.fields) {
      this[name] = json.fields[name];
    }
  }
}

class Photo extends DjangoObject {
  constructor(json) {
    super(json);
  }

  getDirectURL() {
    return `/photo/${this.id}/download`;
  }

  getResizedURL(width, height) {
    return `/photo/${this.id}/shrink/to/fit/${width}x${height}`;
  }

  getThumbnailURL(size) {
    return `/photo/${this.id}/thumbnail/${size}`;
  }
}

const PhotoCache = new Map();
function getPhoto(json) {
  let photo = PhotoCache.get(json.pk);
  if (photo) {
    return photo;
  }

  photo = new Photo(json);
  PhotoCache.set(json.pk, photo);
  return photo;
}

class Folder extends DjangoObject {
  constructor(root, json = undefined) {
    super(json);
    this.root = root;
    this.photos = null;
  }

  async loadPhotos() {
    let json = await fetchJSON(`/${this.root.model}/${this.id}/photos`);
    this.photos = json.map(getPhoto);
  }

  get parentFolder() {
    if (!this.parent) {
      return this.root;
    }
    for (let f of this.root.folders) {
      if (f.id == this.parent) {
        return f;
      }
    }
    return null;
  }

  get subfolders() {
    return this.root.folders.filter(f => f.parent == this.id);
  }
}

class Root extends Folder {
  constructor(model, name) {
    super(null);
    this.id = null;
    this.model = model;
    this.name = name;
    this.folders = [];
  }

  async loadPhotos() {
  }

  async loadFolders() {
    let json = await fetchJSON(`/${this.model}/list`);
    this.folders = json.map(f => new Folder(this, f));
  }

  get parentFolder() {
    return null;
  }

  get subfolders() {
    return this.folders.filter(f => f.parent == null);
  }
}

const ROOTS = [
  new Root("physicalfolder", "All Photos"),
  new Root("tag", "Tags"),
  new Root("person", "People")
];

module.exports = {
  getRoots() {
    return ROOTS;
  }
};
