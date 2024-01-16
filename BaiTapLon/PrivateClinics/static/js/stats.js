function billChart(labels, data){
    const ctx = document.getElementById('billMonthChart');

    new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Doanh thu',
        data: data,
        borderWidth: 1,
        backgroundColor: ['#3c3e3d', '#4e4f42', '#6a44e3']
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

function mediChart(labels, data){
    const ctx = document.getElementById('mediChart');

    new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Số lần dùng',
        data: data,
        borderWidth: 1,
        backgroundColor: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange', 'Black' , 'Pink', 'Brown', 'White', 'Gray', 'Lavender']
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}