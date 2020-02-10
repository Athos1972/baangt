    document.addEventListener('DOMContentLoaded', () => {
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

    // get testrun item
    function load_item(item_type, item_id) {
        const request = new XMLHttpRequest();
        request.open('GET', `/${item_type}/${item_id}`);
        request.onload = () => {
            const response = request.responseText;
            document.querySelector('main').innerHTML = response;
        };
        request.send();
    }

    // create testrun item
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
        var chip_area = document.getElementById(`chips_${name}`);
        var new_chip = document.createElement('div');
        new_chip.setAttribute('class', 'chip mr-1');
        new_chip.setAttribute('data-id', e.options[e.selectedIndex].value);
        new_chip.innerHTML = `
            <small>${e.options[e.selectedIndex].text}</small>
            <span class="closebtn" onclick="delete_chip(this.parentElement, '${name}')">&times;</span>
            `;
        e.options[e.selectedIndex].disabled = true;
        e.selectedIndex = 0;
        chip_area.appendChild(new_chip);
    }

    function delete_chip(e, name) {
        var selector = document.getElementById(name);
        for (var i = 1; i < selector.length; i++) {
            if (selector.options[i].value == e.dataset['id']) {
                selector.options[i].disabled = false;
            }
        }
        e.parentElement.removeChild(e);
    }

    function save_item() {
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
        return true;
    }
// type: "select-multiple"