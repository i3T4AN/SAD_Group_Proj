<template>
  <div :data-theme="theme" class="full-screen offset-top">
    <header>
      <button class="login-button theme-button" @click="openLoginModal">Login</button>
      <h1>Pro Stock Analysis Platform</h1>
    </header>

    <button class="theme-toggle theme-button" @click="toggleTheme">Switch Theme</button>

    <div class="container full-screen reduced-size">
      <div class="search-wrapper">
        <div class="search-bar centered">
          <input
            type="text"
            v-model="stockSymbol"
            placeholder="Search for a stock symbol (e.g., AAPL, TSLA)..."
          />
          <button class="theme-button" @click="addStock">Add Stock</button>
        </div>
      </div>

      <div class="content-wrapper">
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
              <tr v-for="(stock, index) in stockDataList" :key="stock.symbol">
                <td :style="{ color: stockColors[index % stockColors.length] }">{{ stock.symbol }}</td>
                <td :style="{ color: stock.change > 0 ? 'green' : 'red' }">
                  ${{ stock.price.toFixed(2) }}
                </td>
                <td :class="{'positive': stock.change > 0, 'negative': stock.change < 0}">
                  {{ stock.change.toFixed(2) }}%
                </td>
                <td :style="{ color: stock.recommendation === 'Buy' ? 'green' : 'red' }">
                  {{ stock.recommendation }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="chart-container">
          <canvas ref="chartCanvas"></canvas>
        </div>
      </div>
    </div>

    <footer>
      <p>Stock Analysis Platform © 2024</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue';
import Chart from 'chart.js/auto';
import { faker } from '@faker-js/faker';

const themes = ['light', 'dark', 'high-contrast', 'blue', 'green', 'warm'];
const themeIndex = ref(0);
const theme = ref(themes[themeIndex.value]);
const stockColors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'];
const stockSymbol = ref('');
const stockDataList = ref([]);
const chartCanvas = ref(null);
let stockChart = null;

const toggleTheme = async () => {
  themeIndex.value = (themeIndex.value + 1) % themes.length;
  theme.value = themes[themeIndex.value];
  document.querySelector('html').setAttribute('data-theme', theme.value);
  await nextTick();
  applyThemeStyles();
};

const applyThemeStyles = () => {
  const root = document.documentElement;
  root.style.setProperty('--bg-color', getComputedStyle(root).getPropertyValue('--bg-color'));
  root.style.setProperty('--text-color', getComputedStyle(root).getPropertyValue('--text-color'));

  document.querySelectorAll(".theme-button").forEach(button => {
    button.style.backgroundColor = `var(--button-bg)`;
    button.style.color = `var(--text-color)`;
  });
  document.body.style.backgroundColor = `var(--bg-color)`;
  document.body.style.color = `var(--text-color)`;
  updateChart();
};

const generateStockHistory = () => {
  return Array.from({ length: 30 }, (_, i) => ({
    date: new Date(Date.now() - (29 - i) * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
    price: parseFloat(faker.finance.amount(50, 200, 2))
  }));
};

const addStock = async () => {
  if (!stockSymbol.value) return;
  stockDataList.value.push({
    symbol: stockSymbol.value.toUpperCase(),
    price: parseFloat(faker.finance.amount(50, 200, 2)),
    change: parseFloat(faker.finance.amount(-5, 5, 2)),
    recommendation: Math.random() > 0.5 ? 'Buy' : 'Sell',
    history: generateStockHistory()
  });
  stockSymbol.value = '';
  updateChart();
  applyThemeStyles();
};

const updateChart = () => {
  if (!chartCanvas.value) return;
  if (stockChart) stockChart.destroy();

  stockChart = new Chart(chartCanvas.value, {
    type: 'line',
    data: {
      labels: stockDataList.value[0]?.history.map(entry => entry.date) || [],
      datasets: stockDataList.value.map((stock, index) => ({
        label: stock.symbol,
        data: stock.history.map(entry => entry.price),
        borderColor: stockColors[index % stockColors.length],
        backgroundColor: stockColors[index % stockColors.length] + '55',
        fill: true,
      }))
    },
    options: {
      plugins: {
        legend: { labels: { color: `var(--text-color)` } }
      },
      scales: {
        x: { type: 'category', ticks: { color: `var(--text-color)` } },
        y: { ticks: { color: `var(--text-color)` } }
      }
    }
  });
};

onMounted(() => {
  applyThemeStyles();
  updateChart();
});

watch([stockDataList, theme], () => {
  updateChart();
  applyThemeStyles();
}, { deep: true });
</script>

<style>
.positive { color: green; }
.negative { color: red; }
</style>
