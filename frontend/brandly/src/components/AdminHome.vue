<template>
    <div class="admin-home">
        <div class="container h-100 p-4">
            <div class="text-header text-center text-light mb-4">
                <h2>Hey Admin, Here's all you need to know</h2>
            </div>
            <div class="row align-items-start">
                <div class="col-md-4">
                    <div class="card mb-4" v-for="(card, index) in stats" :key="index">
                        <div class="card-body">
                            <h3 class="mb-3">{{ card.title }}</h3>
                            <p>{{ card.value }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-8">
                    <div class="card mb-4">
                        <div class="card-body">
                            <canvas id="lineChart"></canvas>
                        </div>
                    </div>
                    <div class="card">
                        <div class="card-body">
                            <canvas id="pieChart"></canvas>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
import Chart from 'chart.js/auto';

export default {
    name: 'AdminHome',
    data() {
        return {
            stats: [
                { title: 'Active Sponsors', value: 0 },
                { title: 'Active Influencers', value: 0 },
                { title: 'Active Campaigns', value: 0 },
                { title: 'Total Active Users', value: 0 }
            ],
            hourlyRequestData: [],
            pieChartData: {}
        };
    },
    mounted() {
        this.fetchData();
    },
    methods: {
        fetchData() {
            const accessToken = localStorage.getItem('accessToken');
            if (!accessToken) {
                this.$router.push('/login');
                return;
            }

            const requestOptions = {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${accessToken}`,
                    'Content-Type': 'application/json'
                }
            };

            fetch("http://127.0.0.1:8000/api/admin", requestOptions)
                .then(response => response.json())
                .then(result => {
                    console.log(result);
                    this.stats[0].value = result.total_sponsors;
                    this.stats[1].value = result.total_influencers;
                    this.stats[2].value = result.total_campaigns;
                    this.stats[3].value = result.total_users;
                    // sort hourly_request_data by hour
                    result.hourly_request_data.sort((a, b) => a.hour - b.hour);
                    this.hourlyRequestData = result.hourly_request_data;
                    this.pieChartData = result.pie_chart_data;
                    this.renderLineChart();
                    this.renderPieChart();
                })
                .catch(error => console.log('error', error));
        },
        renderLineChart() {
            const ctx = document.getElementById('lineChart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: this.hourlyRequestData.map(data => {
                        // Assume data.hour is an integer representing hours (0-23)
                        const hour = parseInt(data.hour, 10);
                        // Format hour as a time string, e.g., "14:00"
                        return new Date(0, 0, 0, hour).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
                    }),
                    datasets: [{
                        label: 'Hourly Requests',
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        data: this.hourlyRequestData.map(data => data.count)
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        },
        renderPieChart() {
            const ctx = document.getElementById('pieChart').getContext('2d');
            new Chart(ctx, {
                type: 'pie',
                responsive: true,
                data: {
                    labels: ['Influencers', 'Sponsors'],
                    datasets: [{
                        data: [this.pieChartData.influencers, this.pieChartData.sponsors],
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.6)',
                            'rgba(54, 162, 235, 0.6)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: true
                        },
                        title: {
                            display: true,
                            text: 'Influencers : Sponsors',
                            font: {
                                size: 16
                            }
                        }
                    },
                    cutout: '80%',
                    radius: '80%',
                    rotation: -90,
                    circumference: 180
                }
            });
        }
    }
};
</script>

<style scoped>
.admin-home {
    margin: 0;
    margin-top: -1.4rem;
    height: 100%;
    background: linear-gradient(15deg, #5c180f, #7e1a12, #a31a1b, #c51e22) !important;
    scroll-behavior: smooth;
}
.text-header {
    margin-top: 1rem;
}
.card {
    margin-bottom: 1.5rem; /* Adjust margin for spacing between cards */
}
canvas {
    width: 100% !important;
    height: 240px !important; /* Ensure sufficient height for charts */
}
</style>

