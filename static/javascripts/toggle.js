function selectRole(role) {
    document.getElementById('employee').classList.remove('active');
    document.getElementById('reader').classList.remove('active');

    document.getElementById(role).classList.add('active');
    document.getElementById('role').value = role;
}
