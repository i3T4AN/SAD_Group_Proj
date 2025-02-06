<template>
  <div :data-theme="theme">
    <header>
      <h1>Pro Stock Analysis Platform</h1>
      <button @click="openLoginModal">Login</button>
    </header>

    <button class="theme-toggle" @click="toggleTheme">Switch Theme</button>

    <div class="container">
      <div class="search-bar">
        <input
          type="text"
          v-model="stockSymbol"
          placeholder="Search for a stock symbol (e.g., AAPL, TSLA)..."
        />
        <button @click="addStock">Add Stock</button>
      </div>

      <div class="chart-container">
        <canvas ref="chartCanvas"></canvas>
      </div>

      <div class="dashboard">
        <h2>Stock Dashboard</h2>
        <table>
          <thead>
            <tr>
              <th>Symbol</th>
              <th>Price</th>
              <th>Change (%)</th>
              <th>Recommendation</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="stock in stockDataList" :key="stock.symbol">
              <td>{{ stock.symbol }}</td>
              <td>${{ stock.price.toFixed(2) }}</td>
              <td :class="{'positive': stock.change > 0, 'negative': stock.change < 0}">
                {{ stock.change.toFixed(2) }}%
              </td>
              <td>{{ stock.recommendation }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <footer>
      <p>Stock Analysis Platform © 2024</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import Chart from 'chart.js/auto';

const theme = ref('light');
const stockSymbol = ref('');
const stockDataList = ref([]);
const chartCanvas = ref(null);
let stockChart = null;

const toggleTheme = () => {
  theme.value = theme.value === 'light' ? 'dark' : 'light';
};

const fetchStockData = async (symbol) => {
  // Simulated stock data fetching
  const randomPrice = Math.random() * 200 + 50;
  const randomChange = (Math.random() - 0.5) * 5;
  return {
    symbol,
    price: randomPrice,
    change: randomChange,
    recommendation: randomChange > 0 ? 'Buy' : 'Sell',
  };
};

const addStock = async () => {
  if (!stockSymbol.value) return;
  
  const stockData = await fetchStockData(stockSymbol.value.toUpperCase());
  stockDataList.value.push(stockData);
  stockSymbol.value = '';

  updateChart();
};

const updateChart = () => {
  if (!chartCanvas.value) return;

  const labels = stockDataList.value.map(stock => stock.symbol);
  const prices = stockDataList.value.map(stock => stock.price);

  if (stockChart) {
    stockChart.destroy();
  }

  stockChart = new Chart(chartCanvas.value, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: 'Stock Prices',
          data: prices,
          borderColor: 'blue',
          backgroundColor: 'rgba(0, 123, 255, 0.2)',
          fill: true,
        },
      ],
    },
  });
};

onMounted(() => {
  updateChart();
});

watch(stockDataList, updateChart, { deep: true });

const openLoginModal = () => {
  alert('Login functionality is not yet implemented.');
};
</script>

<style scoped>
:root {
  --bg-color: #f4f4f9;
  --text-color: #333;
  --card-bg: #fff;
  --button-bg: #007bff;
  --button-hover: #0056b3;
}
[data-theme="dark"] {
  --bg-color: #1e1e2f;
  --text-color: #f4f4f9;
  --card-bg: #2c2c3c;
  --button-bg: #5b8dfd;
  --button-hover: #3b6fd9;
}
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: var(--bg-color);
  color: var(--text-color);
}
header,
footer {
  padding: 15px;
  background-color: var(--text-color);
  color: var(--bg-color);
  text-align: center;
}
header h1,
footer p {
  margin: 0;
}
.container {
  max-width: 1200px;
  margin: 20px auto;
  padding: 20px;
  background-color: var(--card-bg);
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}
.search-bar {
  text-align: center;
  margin-bottom: 20px;
}
input[type='text'],
button {
  padding: 10px;
  margin: 5px;
  border: 1px solid #ddd;
  border-radius: 5px;
}
button {
  background-color: var(--button-bg);
  color: white;
  cursor: pointer;
}
button:hover {
  background-color: var(--button-hover);
}
.chart-container {
  position: relative;
  height: 400px;
  margin: 20px auto;
}
.dashboard {
  margin-top: 20px;
}
.dashboard table {
  width: 100%;
  border-collapse: collapse;
}
.dashboard th,
.dashboard td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}
.theme-toggle {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 10px;
  cursor: pointer;
  background: var(--button-bg);
  color: var(--bg-color);
  border: none;
  border-radius: 5px;
}
.positive {
  color: green;
}
.negative {
  color: red;
}
</style>
