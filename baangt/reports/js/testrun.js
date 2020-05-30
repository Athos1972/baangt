
    // get item
    function load_item(item_type, item_id) {
        const request = new XMLHttpRequest();
        request.open('GET', `/${item_type}/${item_id}`);
        request.onload = () => {
            const response = request.responseText;
            document.querySelector('main').innerHTML = response;
        };
        request.send();
    }

    // create new item
    function new_item(item_type) {
        const request = new XMLHttpRequest();
        request.open('GET', `/${item_type}/new`);
        request.onload = () => {
            const response = request.responseText;
            document.querySelector('main').innerHTML = response;
        };
        request.send();
    }

    // edit item
    function edit_item(item_type, item_id) {
        const request = new XMLHttpRequest();
        request.open('GET', `/${item_type}/${item_id}/edit`);
        request.onload = () => {
            const response = request.responseText;
            document.querySelector('main').innerHTML = response;
        };
        request.send();
    }

    // delete item
    function set_delete_item(type_name, type, item_id) {
        /* set data in delete modal */
        document.querySelector('#deleteLabel').innerHTML = `Delete ${type_name} ID #${item_id}`;
        const btns = document.querySelector('#deleteButtons');
        btns.setAttribute('data-type', type);
        btns.setAttribute('data-id', item_id);
    }

    function delete_item(e, cascade) {
        /* delete item */
        const request = new XMLHttpRequest();
        if (cascade) {
            // cascade delete: POST request
            request.open('POST', `/${e.dataset['type']}/${e.dataset['id']}/delete`);
        } else {
            // single item delete: DELETE request
            request.open('DELETE', `/${e.dataset['type']}/${e.dataset['id']}/delete`);
        }
        
        request.onload = () => {
            window.location.reload(true); 
        }
        request.send();
    }

    // push message
    function push_message(msg, type) {
        // create message
        var alrt = document.createElement('div');
        alrt.setAttribute('class', `alert alert-${type} alert-dismissible fade show`);
        alrt.setAttribute('role', 'alert');
        alrt.innerHTML = msg;
        // create close button
        var btn = document.createElement('button');
        btn.setAttribute('type', 'button');
        btn.setAttribute('class', 'close');
        btn.setAttribute('data-dismiss', 'alert');
        btn.setAttribute('aria-label', 'Close');
        btn.innerHTML = `<span aria-hidden="true">&times;</span>`;
        // add to main
        alrt.appendChild(btn);
        document.getElementById('flash_area').appendChild(alrt);
    }

    // add DataFile
    function add_datafile() {
        const message = document.getElementById('upload-message');
        const modal = document.getElementById('uploadModal');
        const files = document.getElementById('upload-file').files;
        message.innerHTML = "";
        if (files.length > 0) {
            //console.log(files[0]);
            const request = new XMLHttpRequest();
            request.responseType = 'json';
            request.open('POST', '/datafile/upload');
            // get file
            var datafile = new FormData();
            datafile.append('datafile', files[0]);

            request.onload = () => {
                if (request.status === 200) {
                    // add option to datalist
                    var datalist_option = document.createElement('option');
                    datalist_option.setAttribute('data-id', request.response['id']);
                    datalist_option.innerText = request.response['name'];
                    document.getElementById('datafilesOpt').appendChild(datalist_option);
                    // add option to multi-select
                    var select_option = document.createElement('option');
                    select_option.innerText = request.response['name'];
                    select_option.setAttribute('value', request.response['id']);
                    document.getElementById('datafiles').appendChild(select_option);
                    // message
                    message.innerHTML = '<span class="text-success">DataFile successfully uploaded</span>'
                    document.getElementById('upload-label').innerText = 'Choose a file';
                } else {
                    // push error message
                    for (var key in request.response) {
                        message.innerHTML = `<span class="text-danger">${key.toUpperCase()}: ${request.response[key]}</span>`
                    }
                }
            }
            request.send(datafile);
        } else {
            message.innerHTML = '<span class="text-success">Please select a DataFile</span>';
        }
    }

    function add_datafile_new() {
        const datafiles = document.getElementById('datafiles');
        const files = document.getElementById('datafile-select').files;
        const f = document.querySelector('form');
        var datafile_list = new FormData();
        if (files.length > 0) {
            //datafiles.files.push.apply(files[0]);
            datafile_list.append('file', files[0]);
            //console.log(datafile_list.keys().length);
            //console.log(datafile_list.keys().length);
        } else {
            push_message('No DataFile selected', 'warning');
        }
    }

    function upload_datafile() {
        //console.log('upload');
        const datafiles = document.getElementById('datafiles');
        //document.uploadForm.submit();
    }

    function create_chip(name, text, id) {
        var chip_area = document.getElementById(name);
        var new_chip = document.createElement('div');
        var onclick_action;
        new_chip.setAttribute('class', 'chip mr-1');
        new_chip.setAttribute('data-id', id);
        if (id >= 0) {        
            onclick_action = `delete_chip(this.parentElement, '${name}')`;
        } else {
            onclick_action = 'this.parentElement.remove()';            
        }

        new_chip.innerHTML = `
            <small>${text}</small>
            <span class="closebtn" onclick="${onclick_action}">&times;</span>
            `;
        chip_area.appendChild(new_chip);
    }

    // select multiple with chips
    function add_chip(e, name) {
        // check if option exists
        const text = e.value;
        for (var i = 0; i < e.list.childElementCount; i++) {
            //const opt_text = e.list.children[i].text.toUpperCase();
            if (text === e.list.children[i].text) {
                // create chip
                //create_chip(`chips_${name}`, e.list.children[i].text, i);
                
                var chip_area = document.getElementById(`chips_${name}`);
                var new_chip = document.createElement('div');
                new_chip.setAttribute('class', 'chip mr-1');
                new_chip.setAttribute('data-id', e.list.children[i].dataset['id']);
                new_chip.innerHTML = `
                    <small>${e.list.children[i].text}</small>
                    <span class="closebtn" onclick="delete_chip(this.parentElement, '${name}')">&times;</span>
                    `;
                chip_area.appendChild(new_chip);
                
                // remove selected option from list
                e.value = null;
                e.list.children[i].disabled = true;
                break;
            }
        }
    }

    function delete_chip(e, name) {
        var list = document.getElementById(`${name}Opt`);
        for (var i = 0; i < list.childElementCount; i++) {
            if (e.dataset['id'] === list.children[i].dataset['id']) {
                list.children[i].disabled = false;
                e.parentElement.removeChild(e);
                break;
            }
        }
        
    }

    function get_chips() {
        document.querySelectorAll('datalist').forEach(list => {
            // create multyselect field
            const name = list.id.substring(0, list.id.length - 3);
            const selector = document.getElementById(name);
            const chips_area = document.getElementById(`chips_${name}`);
            //console.log(name);
            chips_area.querySelectorAll('div').forEach(chip => {
                //console.log(chip.dataset['id']);
                //value = chip.dataset['id'];
                for (var i = 0; i < selector.length; i++) {
                    if (chip.dataset['id'] === selector.options[i].value) {
                        selector.options[i].selected = true;
                    }
                }
            });
        });

        return false;
    }

    function filter_options(e) {
        const text = e.value.toUpperCase();
        for (var i = 0; i < e.list.childElementCount; i++) {
            const opt_text = e.list.children[i].text.toUpperCase();
            if (!opt_text.includes(text)) {
                e.list.children[i].style.display = opt_text ? 'list-item' : 'none';
            }


        }
    }

    function filter_items(e) {
        const text = e.value.toUpperCase();
        document.querySelectorAll('.testrun-item').forEach(item => {
            var display = false;
            item.querySelectorAll('.filtered').forEach(property => {
                const value = property.innerHTML.toUpperCase();
                if (value.includes(text)) {
                    display = true;
                }
            });

            item.style.display = display ? '' : 'none';

        });
    }


    function get_file(e) {
        // get filename
        const filename = e.files[0].name;
        const label = e.parentElement.querySelector('label');
        label.innerText = filename;
    }

    function set_export_id(item_id) {
        // set item_id in modal
        const btn = document.querySelector('#exportButton')
        btn.setAttribute('data-id', item_id);
        btn.style.display = '';
        // set modal body
        document.querySelector('#exportRequest').style.display = '';
        document.querySelector('#exportResponse').style.display = 'none';
    }

    function export_item(e) {
        /*
        exports a testrun
        */
        // get export format
        const exportFormat = document.querySelector('input[name="formatRadio"]:checked').value;
        const request = new XMLHttpRequest();
        request.open('GET', `/testrun/${exportFormat}/${e.dataset['id']}`);
        request.onload = () => {
            // get response
            const response = request.responseText;
            // set export modal body 
            const exportResponse = document.querySelector('#exportResponse');
            exportResponse.innerHTML = response;
            exportResponse.style.display = '';
            document.querySelector('#exportRequest').style.display = 'none';
            document.querySelector('#exportButton').style.display = 'none';
        };
        request.send();
    }

    function set_update_item(item_id) {
        document.querySelector('#updateLabel').innerHTML = `Update Testrun ID #${item_id}`;
        document.querySelector('#updateForm').setAttribute('action', `/testrun/${item_id}/import`);
    }

    function add_datafile_link(limit) {
        const active = document.getElementById('activeDataFiles');
        // display DataFile header
        if (active.value == "0") {
            document.getElementById('dataFileHeader').style.display = '';
        }
        // display DataFile field
        document.getElementById(`dataDiv${++active.value}`).style.display = '';
        // check if DataFile number limit achieved
        if (active.value == limit) {
            const link = document.getElementById('dataFileExpander');
            link.setAttribute('class', 'text-muted');
            link.setAttribute('onclick', '');
        } 
    }

    function run_item(item_id) {
        /*
        run the testrun via API web-service
        */
        const request = new XMLHttpRequest();
        request.open('GET', `/testrun/${item_id}/run`);
        request.onload = () => {
            // get response
            const response = request.responseText;
            //document.querySelector('#loading').style.display = 'none';
            //alert(response);
            document.documentElement.innerHTML = response;

        }
        scroll(0, 0);
        document.querySelector('#titleLoading').innerHTML = `Running Testrun ID #${item_id}`;
        document.querySelector('#loading').style.display = 'block';
        
        request.send();

    }