/*   document.addEventListener('DOMContentLoaded', () => {
        // set links
        document.querySelectorAll('.dropdown-item').forEach(link => {
            link.onclick = () => {
                // load item data to main
                load_item(link.dataset.type, link.dataset.id);
                return false;
            };
        });

        document.querySelectorAll('.collapse>.btn').forEach(link => {
            link.onclick = () => {
                // create item
                new_item(link.dataset.type)
                //document.querySelector('main').innerHTML = "Done!"
            };
        });

    });
*/
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

    // select multiple with chips
    function add_chip(e, name) {
        // check if option exists
        const text = e.value;
        for (var i = 0; i < e.list.childElementCount; i++) {
            const opt_text = e.list.children[i].text.toUpperCase();
            if (text === e.list.children[i].text) {
                // create chip
                var chip_area = document.getElementById(`chips_${name}`);
                var new_chip = document.createElement('div');
                new_chip.setAttribute('class', 'chip mr-1');
                new_chip.setAttribute('data-id', i);
                new_chip.innerHTML = `
                    <small>${e.list.children[i].text}</small>
                    <span class="closebtn" onclick="delete_chip(this.parentElement, '${name}')">&times;</span>
                    `;
                chip_area.appendChild(new_chip);
                // remove selected option from list
                e.value = null;
                e.list.children[i].disabled = true;
            }
        }
    }

    function delete_chip(e, name) {
        var list = document.getElementById(`${name}Opt`);
        list.children[e.dataset['id']].disabled = false;
        e.parentElement.removeChild(e);
    }

    function get_chips() {
        document.querySelectorAll('datalist').forEach(list => {
            // create multyselect field
            const name = list.id.substring(0, list.id.length - 3);
            const selector = document.getElementById(name);
            const chips_area = document.getElementById(`chips_${name}`);
            chips_area.querySelectorAll('div').forEach(chip => {
                value = chip.dataset['id'];
                selector.options[value].selected = true;
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

    function exportTestrun(e) {
        const request = new XMLHttpRequest();
        request.open('GET', `/testrun/xlsx/${e.dataset['id']}`);
        request.onload = () => {
            // get request
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