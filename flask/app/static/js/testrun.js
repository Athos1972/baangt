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
    function delete_item(item_type, item_name, item_id) {
        if (confirm(`You are about to delete '${item_name}'`)) {
            const request = new XMLHttpRequest();
            request.open('POST', `/${item_type}/${item_id}/delete`);
            request.onload = () => {
                const response = request.responseText;
                document.write(response);
            }
            request.send();
        };
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
        /*
        for (var i = 1; i < list.childElementCount; i++) {
            if (list.children[i].text == e.dataset['id']) {
                list.children[i].disabled = false;
            }
        }
        */
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


/*
        document.querySelectorAll('.multyselect').forEach(selector => {
            selector.setAttribute('multiple','');
            selector.options[0].selected = false;
            for (var i = 1; i < selector.length; i++) {
                if (selector.options[i].disabled) {
                    selector.options[i].disabled = false;
                    selector.options[i].selected = true;
                }
            }
            console.log("Ok!");
        });
*/
        return false;
    }

    function filter_options(e) {
        const text = e.value.toUpperCase();
        for (var i = 0; i < e.list.childElementCount; i++) {
            const opt_text = e.list.children[i].text.toUpperCase();
            if (!opt_text.includes(text)) {
                e.list.children[i].style.display = opt_text ? 'list-item':'none';
            }


        }
    }
// type: "select-multiple"