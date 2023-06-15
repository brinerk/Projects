var customStyles = document.createElement('style');

document.body.insertBefore(customStyles, document.body.firstChild);

customStyles.innerHTML += ".ytd-watch-next-secondary-results-renderer { display: none; }";
//customStyles.innerHTML += ".ytd-comments { display: none; }";
