// Scripts for slide out menu

var sideNav = document.getElementById('side-nav');
var menuExpander = document.getElementById('menu-expander');

function toggleMenu() {
  if (sideNav.style.left == '-220px') {
    sideNav.style.left = '0';
    menuExpander.style.left = '232px';
    menuExpander.style.backgroundColor = 'rgba(204,165,89,0.9)';
  } else {
    sideNav.style.left = '-220px';
    menuExpander.style.left = '12px';
    menuExpander.style.removeProperty('background-color');
  }
}

// Scripts for modal iframe windows
var modalWindow = document.getElementById('modal-window');
var modaliFrame = document.getElementById('modal-iframe');

window.addEventListener('click', outsideClick);

function openModalDate(year, month, day) {
  // set blank modal display; set src of iframe so that it loads...
  modaliFrame.src = '/' + year + '-' + month + '-' + day;
  modalWindow.style.display = 'block';
}

function openModalOther(page) {
  // open modal for the login page
  modaliFrame.src = '/' + page;
  modalWindow.style.display = 'block';
}

function closeModal() {
  parent.location.reload();
}

function outsideClick (e) {
  if (e.target == modalWindow) {
    modalWindow.style.display = 'none';
  }
}
