    document.addEventListener('DOMContentLoaded', () => {
        // set links
        document.querySelectorAll('.dropdown-item').forEach(link => {
            link.onclick = () => {
                //const content = 'Testrun';
                //document.querySelector('#dataArea').innerHTML = content;
                load_testrun(link.dataset.type, link.dataset.id);
                return false;
            };
        });
    });

    // get testrun
    function load_testrun(item_type, item_id) {
        const request = new XMLHttpRequest();
        request.open('GET', `/${item_type}/${item_id}`);
        request.onload = () => {
            const response = request.responseText;
            document.querySelector('main').innerHTML = response;
        };
        request.send();
    }