// Tab Navigation
document.addEventListener('DOMContentLoaded', function() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // Remove active class from all buttons and panes
            tabBtns.forEach(b => b.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('active'));

            // Add active class to clicked button and corresponding pane
            btn.classList.add('active');
            const tabId = btn.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');

            // Re-initialize charts for the active tab
            if (tabId === 'overview') {
                createFlightVolumeChart();
                createDelayDistributionChart();
            } else if (tabId === 'bengaluru') {
                createBengaluruCharts();
            } else if (tabId === 'delhi') {
                createDelhiCharts();
            } else if (tabId === 'comparison') {
                createComparisonCharts();
            }
        });
    });

    // Initialize charts for the default active tab
    createFlightVolumeChart();
    createDelayDistributionChart();
    
    // Initialize chatbot
    initializeChatbot();
    
    // Update overview statistics with real data
    updateOverviewStats();
    
    // Handle window resize for high DPI support
    window.addEventListener('resize', () => {
        setTimeout(() => {
            setupHighDPI();
        }, 100);
    });
});

// Chart.js Configuration
Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
Chart.defaults.color = '#333';
Chart.defaults.plugins.legend.position = 'bottom';

// Improve chart resolution and quality
Chart.defaults.responsive = true;
Chart.defaults.maintainAspectRatio = true;
Chart.defaults.devicePixelRatio = window.devicePixelRatio || 1;
Chart.defaults.elements.point.radius = 4;
Chart.defaults.elements.point.hoverRadius = 6;
Chart.defaults.elements.line.borderWidth = 2;
Chart.defaults.elements.bar.borderWidth = 1;

// Setup high DPI support for better chart resolutioon
function setupHighDPI() {
    const canvases = document.querySelectorAll('canvas');
    canvases.forEach(canvas => {
        const ctx = canvas.getContext('2d');
        const dpr = window.devicePixelRatio || 1;
        const rect = canvas.getBoundingClientRect();
        
        canvas.width = rect.width * dpr;
        canvas.height = rect.height * dpr;
        ctx.scale(dpr, dpr);
    });
}

// Initialize all charts
async function initializeCharts() {
    try {
        // Setup high DPI support
        setupHighDPI();
        
        // Load real data from JSON file
        const response = await fetch('dashboard_stats.json');
        const stats = await response.json();
        
        createFlightVolumeChart(stats);
        createDelayDistributionChart(stats);
        createBengaluruCharts(stats);
        createDelhiCharts(stats);
        createComparisonCharts(stats);
    } catch (error) {
        console.error('Error loading data:', error);
        // Fallback to default data if JSON loading fails
        createFlightVolumeChart();
        createDelayDistributionChart();
        createBengaluruCharts();
        createDelhiCharts();
        createComparisonCharts();
    }
}

// Overview Charts
function createFlightVolumeChart(stats = null) {
    const ctx = document.getElementById('flightVolumeChart').getContext('2d');
    
    let data = [5174, 8709];
    if (stats && stats.flight_counts) {
        data = [stats.flight_counts.BLR, stats.flight_counts.DEL];
    }
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Bengaluru (BLR)', 'Delhi (DEL)'],
            datasets: [{
                label: 'Total Flights',
                data: data,
                backgroundColor: [
                    'rgba(102, 126, 234, 0.8)',
                    'rgba(118, 75, 162, 0.8)'
                ],
                borderColor: [
                    'rgba(102, 126, 234, 1)',
                    'rgba(118, 75, 162, 1)'
                ],
                borderWidth: 2,
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            devicePixelRatio: window.devicePixelRatio || 2,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)',
                        lineWidth: 1
                    },
                    ticks: {
                        font: {
                            size: 12
                        }
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            size: 12
                        }
                    }
                }
            },
            elements: {
                bar: {
                    borderWidth: 1,
                    borderRadius: 8
                }
            }
        }
    });
}

function createDelayDistributionChart(stats = null) {
    const ctx = document.getElementById('delayDistributionChart').getContext('2d');
    
    let blrData = [0.015, 0.736, 0.188, 0.035, 0.012, 0.009, 0.003, 0.001];
    let delData = [0.792, 0.104, 0.033, 0.032, 0.014, 0.007, 0.004, 0.002];
    let labels = ['-60', '-30', '0', '30', '60', '90', '120', '150'];
    
    if (stats && stats.delay_distribution) {
        blrData = stats.delay_distribution.BLR;
        delData = stats.delay_distribution.DEL;
        labels = stats.delay_distribution.labels;
    }
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Bengaluru',
                data: blrData,
                borderColor: 'rgba(102, 126, 234, 1)',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                fill: true,
                tension: 0.4
            }, {
                label: 'Delhi',
                data: delData,
                borderColor: 'rgba(118, 75, 162, 1)',
                backgroundColor: 'rgba(118, 75, 162, 0.1)',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            devicePixelRatio: window.devicePixelRatio || 2,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        font: {
                            size: 12
                        },
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Density',
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)',
                        lineWidth: 1
                    },
                    ticks: {
                        font: {
                            size: 12
                        }
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Delay (minutes)',
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)',
                        lineWidth: 1
                    },
                    ticks: {
                        font: {
                            size: 12
                        }
                    }
                }
            },
            elements: {
                line: {
                    borderWidth: 3,
                    tension: 0.4
                },
                point: {
                    radius: 4,
                    hoverRadius: 6,
                    borderWidth: 2
                }
            }
        }
    });
}

// Bengaluru Charts
function createBengaluruCharts(stats = null) {
    // Flight Type Distribution
    const flightTypeCtx = document.getElementById('blrFlightTypeChart').getContext('2d');
    
    let labels = ['Departure', 'Arrival'];
    let data = [2649, 2525];
    
    if (stats && stats.flight_type_distribution && stats.flight_type_distribution.BLR) {
        labels = stats.flight_type_distribution.BLR.labels;
        data = stats.flight_type_distribution.BLR.data;
    }
    
    new Chart(flightTypeCtx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: [
                    'rgba(102, 126, 234, 0.8)',
                    'rgba(255, 107, 107, 0.8)'
                ],
                borderColor: [
                    'rgba(102, 126, 234, 1)',
                    'rgba(255, 107, 107, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            devicePixelRatio: window.devicePixelRatio || 2,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        font: {
                            size: 12
                        },
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                }
            },
            elements: {
                arc: {
                    borderWidth: 2
                }
            }
        }
    });

    // Top Airlines - Using exact data from the image
    const airlinesCtx = document.getElementById('blrAirlinesChart').getContext('2d');
    
    let airlineLabels = ['IndiGo', 'Air India Express', 'Air India', 'Starlight Airline', 'AKJ', 'Shuttle America', 'Alliance Air', 'Emirates'];
    let airlineData = [2703, 762, 511, 415, 136, 64, 49, 42];
    
    if (stats && stats.top_airlines && stats.top_airlines.BLR) {
        airlineLabels = stats.top_airlines.BLR.labels;
        airlineData = stats.top_airlines.BLR.data;
    }
    
    new Chart(airlinesCtx, {
        type: 'bar',
        data: {
            labels: airlineLabels,
            datasets: [{
                label: 'Number of Flights',
                data: airlineData,
                backgroundColor: 'rgba(102, 126, 234, 0.8)',
                borderColor: 'rgba(102, 126, 234, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            devicePixelRatio: window.devicePixelRatio || 2,
            indexAxis: 'y',
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Flights',
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)',
                        lineWidth: 1
                    },
                    ticks: {
                        font: {
                            size: 12
                        }
                    }
                },
                y: {
                    ticks: {
                        font: {
                            size: 12
                        }
                    }
                }
            },
            elements: {
                bar: {
                    borderWidth: 1
                }
            }
        }
    });

    // Hourly Traffic Pattern - Using exact data from the image
    const hourlyCtx = document.getElementById('blrHourlyChart').getContext('2d');
    
    let hourlyLabels = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'];
    let hourlyData = [52, 41, 27, 38, 86, 171, 197, 135, 174, 97, 173, 120, 134, 130, 101, 143, 106, 104, 148, 119, 153, 86, 66, 48];
    
    if (stats && stats.hourly_traffic && stats.hourly_traffic.BLR) {
        hourlyLabels = stats.hourly_traffic.labels;
        hourlyData = stats.hourly_traffic.BLR;
    }
    
    new Chart(hourlyCtx, {
        type: 'line',
        data: {
            labels: hourlyLabels,
            datasets: [{
                label: 'Flight Count',
                data: hourlyData,
                borderColor: 'rgba(102, 126, 234, 1)',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            devicePixelRatio: window.devicePixelRatio || 2,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Flights',
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)',
                        lineWidth: 1
                    },
                    ticks: {
                        font: {
                            size: 12
                        }
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Hour of Day',
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)',
                        lineWidth: 1
                    },
                    ticks: {
                        font: {
                            size: 12
                        }
                    }
                }
            },
            elements: {
                line: {
                    borderWidth: 3,
                    tension: 0.4
                },
                point: {
                    radius: 3,
                    hoverRadius: 5,
                    borderWidth: 2
                }
            }
        }
    });

    // Delay Heatmap - Creating heatmap data based on the image
    const heatmapCtx = document.getElementById('blrDelayHeatmap').getContext('2d');
    
    // Create heatmap data for 24 hours
    const heatmapLabels = Array.from({length: 24}, (_, i) => i.toString());
    const heatmapData = [
        // Bangalore delay data (approximated from the image)
        5, 6, 7, 8, 4, 3, 2, 1, 0, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14
    ];
    
    new Chart(heatmapCtx, {
        type: 'bar',
        data: {
            labels: heatmapLabels,
            datasets: [{
                label: 'Average Delay (min)',
                data: heatmapData,
                backgroundColor: heatmapData.map(delay => {
                    if (delay < 0) return 'rgba(76, 175, 80, 0.8)'; // Green for negative
                    if (delay < 5) return 'rgba(255, 255, 0, 0.8)'; // Yellow for low
                    if (delay < 10) return 'rgba(255, 152, 0, 0.8)'; // Orange for medium
                    return 'rgba(244, 67, 54, 0.8)'; // Red for high
                }),
                borderColor: heatmapData.map(delay => {
                    if (delay < 0) return 'rgba(76, 175, 80, 1)';
                    if (delay < 5) return 'rgba(255, 255, 0, 1)';
                    if (delay < 10) return 'rgba(255, 152, 0, 1)';
                    return 'rgba(244, 67, 54, 1)';
                }),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            devicePixelRatio: window.devicePixelRatio || 2,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Delay (minutes)',
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)',
                        lineWidth: 1
                    },
                    ticks: {
                        font: {
                            size: 12
                        }
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Hour of Day',
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)',
                        lineWidth: 1
                    },
                    ticks: {
                        font: {
                            size: 12
                        }
                    }
                }
            },
            elements: {
                bar: {
                    borderWidth: 1
                }
            }
        }
    });
}

// Delhi Charts
function createDelhiCharts(stats = null) {
    // Flight Type Distribution
    const flightTypeCtx = document.getElementById('delFlightTypeChart').getContext('2d');
    
    let labels = ['Departure', 'Arrival'];
    let data = [4393, 4316];
    
    if (stats && stats.flight_type_distribution && stats.flight_type_distribution.DEL) {
        labels = stats.flight_type_distribution.DEL.labels;
        data = stats.flight_type_distribution.DEL.data;
    }
    
    new Chart(flightTypeCtx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: [
                    'rgba(118, 75, 162, 0.8)',
                    'rgba(255, 193, 7, 0.8)'
                ],
                borderColor: [
                    'rgba(118, 75, 162, 1)',
                    'rgba(255, 193, 7, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });

    // Top Airlines - Using exact data from JSON
    const airlinesCtx = document.getElementById('delAirlinesChart').getContext('2d');
    
    let airlineLabels = ['IndiGo', 'Air India', 'Air India Express', 'SpiceJet', 'ZZ', 'Starlight Airline', 'Alliance Air', 'Etihad'];
    let airlineData = [3134, 2931, 623, 377, 267, 249, 147, 56];
    
    if (stats && stats.top_airlines && stats.top_airlines.DEL) {
        airlineLabels = stats.top_airlines.DEL.labels;
        airlineData = stats.top_airlines.DEL.data;
    }
    
    new Chart(airlinesCtx, {
        type: 'bar',
        data: {
            labels: airlineLabels,
            datasets: [{
                label: 'Number of Flights',
                data: airlineData,
                backgroundColor: 'rgba(118, 75, 162, 0.8)',
                borderColor: 'rgba(118, 75, 162, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'y',
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Flights'
                    }
                }
            }
        }
    });

    // Hourly Traffic Pattern - Using exact data from JSON
    const hourlyCtx = document.getElementById('delHourlyChart').getContext('2d');
    
    let hourlyLabels = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'];
    let hourlyData = [47, 67, 96, 91, 152, 232, 240, 217, 264, 235, 213, 171, 224, 239, 201, 167, 218, 207, 242, 209, 216, 224, 102, 119];
    
    if (stats && stats.hourly_traffic && stats.hourly_traffic.DEL) {
        hourlyLabels = stats.hourly_traffic.labels;
        hourlyData = stats.hourly_traffic.DEL;
    }
    
    new Chart(hourlyCtx, {
        type: 'line',
        data: {
            labels: hourlyLabels,
            datasets: [{
                label: 'Flight Count',
                data: hourlyData,
                borderColor: 'rgba(118, 75, 162, 1)',
                backgroundColor: 'rgba(118, 75, 162, 0.1)',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Flights'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Hour of Day'
                    }
                }
            }
        }
    });

    // Delay Heatmap - Creating heatmap data based on the image
    const heatmapCtx = document.getElementById('delDelayHeatmap').getContext('2d');
    
    // Create heatmap data for 24 hours
    const heatmapLabels = Array.from({length: 24}, (_, i) => i.toString());
    const heatmapData = [
        // Delhi delay data (approximated from the image)
        8, 9, 10, 11, 7, 6, 5, 4, 3, 2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14
    ];
    
    new Chart(heatmapCtx, {
        type: 'bar',
        data: {
            labels: heatmapLabels,
            datasets: [{
                label: 'Average Delay (min)',
                data: heatmapData,
                backgroundColor: heatmapData.map(delay => {
                    if (delay < 0) return 'rgba(76, 175, 80, 0.8)'; // Green for negative
                    if (delay < 5) return 'rgba(255, 255, 0, 0.8)'; // Yellow for low
                    if (delay < 10) return 'rgba(255, 152, 0, 0.8)'; // Orange for medium
                    return 'rgba(244, 67, 54, 0.8)'; // Red for high
                }),
                borderColor: heatmapData.map(delay => {
                    if (delay < 0) return 'rgba(76, 175, 80, 1)';
                    if (delay < 5) return 'rgba(255, 255, 0, 1)';
                    if (delay < 10) return 'rgba(255, 152, 0, 1)';
                    return 'rgba(244, 67, 54, 1)';
                }),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Delay (minutes)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Hour of Day'
                    }
                }
            }
        }
    });
}

// Comparison Charts
function createComparisonCharts(stats = null) {
    // On-Time Performance Comparison
    const ontimeCtx = document.getElementById('ontimeComparisonChart').getContext('2d');
    
    let blrData = [88.5, 8.9, 2.6];
    let delData = [82.9, 10.5, 6.6];
    
    if (stats && stats.ontime_performance) {
        blrData = [stats.ontime_performance.BLR.on_time, stats.ontime_performance.BLR.delayed, stats.ontime_performance.BLR.cancelled];
        delData = [stats.ontime_performance.DEL.on_time, stats.ontime_performance.DEL.delayed, stats.ontime_performance.DEL.cancelled];
    }
    
    new Chart(ontimeCtx, {
        type: 'bar',
        data: {
            labels: ['On-Time', 'Delayed', 'Cancelled'],
            datasets: [{
                label: 'Bengaluru',
                data: blrData,
                backgroundColor: 'rgba(102, 126, 234, 0.8)',
                borderColor: 'rgba(102, 126, 234, 1)',
                borderWidth: 2
            }, {
                label: 'Delhi',
                data: delData,
                backgroundColor: 'rgba(118, 75, 162, 0.8)',
                borderColor: 'rgba(118, 75, 162, 1)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    title: {
                        display: true,
                        text: 'Percentage (%)'
                    }
                }
            }
        }
    });

    // Average Delay by Carrier
    const carrierCtx = document.getElementById('carrierDelayChart').getContext('2d');
    
    let carrierLabels = ['IndiGo', 'Air India', 'Air India Express', 'SpiceJet', 'Starlight Airline'];
    let blrCarrierData = [0.93, 5.68, -1.13, 0, 4.47];
    let delCarrierData = [0.48, 8.34, 2.47, 34.72, 0];
    
    if (stats && stats.carrier_delays) {
        carrierLabels = Object.keys(stats.carrier_delays.BLR);
        blrCarrierData = Object.values(stats.carrier_delays.BLR);
        delCarrierData = Object.values(stats.carrier_delays.DEL);
    }
    
    new Chart(carrierCtx, {
        type: 'bar',
        data: {
            labels: carrierLabels,
            datasets: [{
                label: 'Bengaluru',
                data: blrCarrierData,
                backgroundColor: 'rgba(102, 126, 234, 0.8)',
                borderColor: 'rgba(102, 126, 234, 1)',
                borderWidth: 1
            }, {
                label: 'Delhi',
                data: delCarrierData,
                backgroundColor: 'rgba(118, 75, 162, 0.8)',
                borderColor: 'rgba(118, 75, 162, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Average Delay (minutes)'
                    }
                }
            }
        }
    });

    // Hourly Traffic Pattern Comparison (replacing daily trend)
    const trendCtx = document.getElementById('dailyTrendChart').getContext('2d');
    
    let hourlyLabels = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'];
    let blrHourlyData = [52, 41, 27, 38, 86, 171, 197, 135, 174, 97, 173, 120, 134, 130, 101, 143, 106, 104, 148, 119, 153, 86, 66, 48];
    let delHourlyData = [47, 67, 96, 91, 152, 232, 240, 217, 264, 235, 213, 171, 224, 239, 201, 167, 218, 207, 242, 209, 216, 224, 102, 119];
    
    if (stats && stats.hourly_traffic) {
        hourlyLabels = stats.hourly_traffic.labels;
        blrHourlyData = stats.hourly_traffic.BLR;
        delHourlyData = stats.hourly_traffic.DEL;
    }
    
    new Chart(trendCtx, {
        type: 'bar',
        data: {
            labels: hourlyLabels,
            datasets: [{
                label: 'Bengaluru',
                data: blrHourlyData,
                backgroundColor: 'rgba(102, 126, 234, 0.6)',
                borderColor: 'rgba(102, 126, 234, 1)',
                borderWidth: 1
            }, {
                label: 'Delhi',
                data: delHourlyData,
                backgroundColor: 'rgba(118, 75, 162, 0.6)',
                borderColor: 'rgba(118, 75, 162, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Flights'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Hour of Day'
                    }
                }
            }
        }
    });

    // Delay Severity Distribution
    const severityCtx = document.getElementById('delaySeverityChart').getContext('2d');
    
    let severityLabels = ['On-Time', 'Delayed', 'Cancelled'];
    let blrSeverityData = [88.5, 8.9, 2.6];
    let delSeverityData = [82.9, 10.5, 6.6];
    
    if (stats && stats.delay_severity) {
        blrSeverityData = stats.delay_severity.BLR;
        delSeverityData = stats.delay_severity.DEL;
    }
    
    new Chart(severityCtx, {
        type: 'doughnut',
        data: {
            labels: severityLabels,
            datasets: [{
                data: blrSeverityData,
                backgroundColor: [
                    'rgba(76, 175, 80, 0.8)',
                    'rgba(255, 152, 0, 0.8)',
                    'rgba(244, 67, 54, 0.8)'
                ],
                borderColor: [
                    'rgba(76, 175, 80, 1)',
                    'rgba(255, 152, 0, 1)',
                    'rgba(244, 67, 54, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// Update Overview Statistics
async function updateOverviewStats() {
    try {
        const response = await fetch('dashboard_stats.json');
        const stats = await response.json();
        
        // Update total flights
        document.getElementById('totalFlights').textContent = stats.flight_counts.total.toLocaleString();
        
        // Calculate average delay across both airports (weighted by flight count)
        const blrTotalFlights = stats.flight_counts.BLR;
        const delTotalFlights = stats.flight_counts.DEL;
        const totalFlights = blrTotalFlights + delTotalFlights;
        
        const blrAvgDelay = (stats.delay_stats.BLR.avg_departure_delay + stats.delay_stats.BLR.avg_arrival_delay) / 2;
        const delAvgDelay = (stats.delay_stats.DEL.avg_departure_delay + stats.delay_stats.DEL.avg_arrival_delay) / 2;
        const overallAvgDelay = (blrAvgDelay * blrTotalFlights + delAvgDelay * delTotalFlights) / totalFlights;
        document.getElementById('avgDelay').textContent = overallAvgDelay.toFixed(1);
        
        // Calculate overall on-time performance (weighted by flight count)
        const blrOntime = stats.ontime_performance.BLR.on_time;
        const delOntime = stats.ontime_performance.DEL.on_time;
        const overallOntime = (blrOntime * blrTotalFlights + delOntime * delTotalFlights) / totalFlights;
        document.getElementById('ontimeRate').textContent = overallOntime.toFixed(1) + '%';
        
        // Update Bengaluru stats
        document.getElementById('blrTotalFlights').textContent = stats.flight_counts.BLR.toLocaleString();
        document.getElementById('blrAvgDelay').textContent = blrAvgDelay.toFixed(1);
        document.getElementById('blrOntimeRate').textContent = blrOntime.toFixed(1) + '%';
        
        // Update Delhi stats
        document.getElementById('delTotalFlights').textContent = stats.flight_counts.DEL.toLocaleString();
        document.getElementById('delAvgDelay').textContent = delAvgDelay.toFixed(1);
        document.getElementById('delOntimeRate').textContent = delOntime.toFixed(1) + '%';
        
    } catch (error) {
        console.error('Error updating overview stats:', error);
    }
}

// Chatbot Functionality with Simple RAG Pipeline
function initializeChatbot() {
    const chatbotToggle = document.getElementById('chatbotToggle');
    const chatbotPanel = document.getElementById('chatbotPanel');
    const closeChatbot = document.getElementById('closeChatbot');
    const chatInput = document.getElementById('chatInput');
    const sendMessage = document.getElementById('sendMessage');
    const chatMessages = document.getElementById('chatMessages');
    const GROQ_API_KEY = '';//redacteed
    const GROQ_ENDPOINT = 'https://api.groq.com/openai/v1/chat/completions';
    const GROQ_MODEL = 'llama-3.3-70b-versatile';
  
    let contextChunks = [];
  
    async function loadContextChunks() {
      try {
        const response = await fetch('data/context.txt', { cache: 'no-store' });
        if (!response.ok) {
          contextChunks = [];
          return;
        }
        const contextText = await response.text();
        contextChunks = contextText.split(/(?<=[.?!])\s+/).map(s => s.trim()).filter(s => s.length > 0);
      } catch {
        contextChunks = [];
      }
    }
  
    loadContextChunks();
  
    chatbotToggle.addEventListener('click', () => {
      chatbotPanel.classList.add('active');
    });
  
    closeChatbot.addEventListener('click', () => {
      chatbotPanel.classList.remove('active');
    });
  
    function addMessage(text, sender) {
      const messageDiv = document.createElement('div');
      messageDiv.className = `message ${sender}-message`;
      const icon = sender === 'bot' ? 'fas fa-robot' : 'fas fa-user';
      messageDiv.innerHTML = `
        <div class="message-content">
          <i class="${icon}"></i>
          <p>${text}</p>
        </div>
      `;
      chatMessages.appendChild(messageDiv);
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }
  
    function sendChatMessage() {
      const message = chatInput.value.trim();
      if (!message) return;
      addMessage(message, 'user');
      chatInput.value = '';
      setTimeout(async () => {
        if (!contextChunks.length) await loadContextChunks();
        const response = await generateBotResponseRAG(message, contextChunks);
        addMessage(response, 'bot');
      }, 200);
    }
  
    sendMessage.addEventListener('click', sendChatMessage);
    chatInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') sendChatMessage();
    });
  
    function tokenize(text) {
      const stop = new Set([
        'the','and','for','are','with','that','this','your','from','was','were','have','has','had','not','but','its','can','will','would','could','a','an','of','to','in','on','at','by','or','as','it','be','is','am','we','our','they','them','their','there','here','than','then','over','under','into','out','about','also','any','all','more','most','some','such','if','so'
      ]);
      return text.toLowerCase().replace(/[^\w\s]/g, ' ').split(/\s+/).filter(w => w.length > 2 && !stop.has(w));
    }
  
    function scoreChunks(queryTokens, chunks) {
      return chunks.map(chunk => {
        const tokens = tokenize(chunk);
        const set = new Set(tokens);
        let score = 0;
        for (const q of queryTokens) if (set.has(q)) score += 1;
        return { chunk, score };
      });
    }
  
    async function generateBotResponseRAG(message, chunks) {
      const queryTokens = tokenize(message);
      const scored = scoreChunks(queryTokens, chunks).filter(s => s.score > 0).sort((a, b) => b.score - a.score);
      const topK = 3;
      const topChunks = scored.slice(0, topK).map(s => s.chunk);
      const contextText = topChunks.length ? topChunks.join('\n') : '';
      const systemPrompt = "You are an expert assistant for an airport analytics dashboard. Use the provided context to answer the user's question as accurately as possible. If the context is insufficient, say so politely.";
      const userPrompt = `User question: ${message}
  
  Relevant context:
  ${contextText}`;
      try {
        const resp = await fetch(GROQ_ENDPOINT, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${GROQ_API_KEY}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            model: GROQ_MODEL,
            messages: [
              { role: 'system', content: systemPrompt },
              { role: 'user', content: userPrompt }
            ],
            max_tokens: 512,
            temperature: 0.7,
            top_p: 1
          })
        });
        if (!resp.ok) {
          const errText = await resp.text();
          return `Sorry, there was an error connecting to the Groq API: ${errText}`;
        }
        const data = await resp.json();
        const content = data?.choices?.[0]?.message?.content?.trim();
        return content || "Sorry, I couldn't generate a response at this time.";
      } catch {
        return "Sorry, there was a problem reaching the Groq API.";
      }
    }
  }
  
