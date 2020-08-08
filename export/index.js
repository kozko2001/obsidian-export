const Dropbox = require('dropbox').Dropbox;
const fetch = require('isomorphic-fetch');
const fs = require('fs');

const ACCESS_TOKEN = process.env.DROPBOX_ACCESS_TOKEN;
const DROPBOX_PATH = process.env.DROPBOX_PATH || '/obsidian/obsidian-notes'

new Dropbox({
  fetch,
  accessToken: ACCESS_TOKEN,
})
  .filesDownloadZip({path: DROPBOX_PATH})
  .then((result, error) => {
    if(error) {
      console.error(error);
      process.exit(1);
    }

    fs.writeFile('data.zip', result.fileBinary, 'binary', function (err) {
      if (err) { throw err; }
      console.log('File saved.');
    });
  })
  .catch(e => {
    console.error(e);
    process.exit(1);
  });