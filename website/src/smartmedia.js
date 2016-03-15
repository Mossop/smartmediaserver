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

function convertObject(root, parent, json) {
  switch (json.model) {
    case "website.photo":
      return getPhoto(json);
    default:
      return new Folder(root, parent, json);
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
  constructor(root = null, parent = null, json = null) {
    super(json);
    this.root = root;
    this.parent = parent;
    this.contents = [];
  }

  get contentURL() {
    return `/${this.root.model}/${this.id}/contents`;
  }

  async loadContents() {
    let json = await fetchJSON(this.contentURL);
    this.contents = json.map(o => convertObject(this.root, this, o));
  }

  get subfolders() {
    return this.contents.filter(i => i instanceof Folder);
  }

  get photos() {
    return this.contents.filter(i => i instanceof Photo);
  }
}

class Root extends Folder {
  constructor(model, name) {
    super();
    this.root = this;
    this.id = model;
    this.model = model;
    this.name = name;
  }

  get contentURL() {
    return `/${this.model}/contents`;
  }

  get parentFolder() {
    return null;
  }
}

module.exports = {
  async loadRoots() {
    let json = await fetchJSON(`/list/roots`);
    return json.map(r => new Root(r.model, r.name));
  }
};
