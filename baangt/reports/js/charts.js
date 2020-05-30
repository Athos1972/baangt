document.addEventListener('DOMContentLoaded', () => {
    
    document.querySelectorAll('.hovered-item').forEach(item => {
        console.log(item.id);
        // get chart data
        const request = new XMLHttpRequest();
        request.responseType = 'json';
        request.open('POST', `/chart/${item.id}`);
        request.onload = () => {
            // customize legend
            var duration = request.response['duration'];
            duration['options']['tooltips']['callbacks'] = {
                label: function(item, data) {
                    var label = data.datasets[item.datasetIndex].label || '';
                    if (label) {
                        label += ': ';
                    }
                    label += item.value;
                    label += ' sec';

                    return label;
                }
            };
            //console.log(results['options']['tooltips']);
            // draw charts 
            var statusChart = new Chart(item.querySelector('.statusChart'), request.response['status']);
            var resultsChart = new Chart(item.querySelector('.resultsChart'), request.response['results']);
            var durationChart = new Chart(item.querySelector('.durationChart'), duration);
        };
        request.send();
    });
});