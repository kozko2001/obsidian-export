const Dropbox = require('dropbox').Dropbox;
const fetch = require('isomorphic-fetch');
const trello = require('trello-to-markdown-table');

const ACCESS_TOKEN = process.env.DROPBOX_ACCESS_TOKEN;
const DROPBOX_PATH = process.env.DROPBOX_PATH || '/obsidian/obsidian-notes'

const TRELLO_API = process.env.TRELLO_API;
const TRELLO_SECRET = process.env.TRELLO_SECRET;

const dbx = new Dropbox({
    fetch,
    accessToken: ACCESS_TOKEN,
})

const board = "C5eJ2nzP";

trello(TRELLO_API, TRELLO_SECRET, board)
    .then(out => dbx.filesUpload({ path: DROPBOX_PATH + '/Personal Kanban.md', contents: out, mode: 'overwrite'}))
    .then(() => console.log("done!"))
    .catch((e) => console.log("error found... ", e))
