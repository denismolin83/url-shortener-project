<template>
  <div class="container">
    <h1>Сократитель ссылок</h1>

    <div class="input-group">
      <input
        v-model="longUrl"
        type="text"
        placeholder="Вставьте длинную сслыку (например, google.com)"
        @keyup.enter="shortenUrl"
      />
      <button @click="shortenUrl" :disabled="loading">
        {{ loading ? 'Сокращаем...' : 'Сократить' }}
      </button>
    </div>

    <div v-if="shortenedUrl" class="result">
      <p>Ваша ссылка готова:</p>
      <a :href="shortenedUrl" target="_blank">{{ shortenedUrl }}</a>
    </div>

    <div v-if="error" class="error">
      {{ error }}
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const longUrl = ref('')
const shortenedUrl = ref('')
const loading = ref(false)
const error = ref('')

const shortenUrl = async () => {
  if (!longUrl.value) return

  error.value = ''
  shortenedUrl.value = ''

  const urlPattern = /^(https?:\/\/)[^\s$.?#].[^\s]*$/;
  if (!urlPattern.test(longUrl.value)) {
    error.value = 'Пожалуйста, введите корректный URL (начиная с http:// или https://)';
    return;
  }

  loading.value = true

  try {
    const response = await axios.post('/api/shorten', {
      target_url: longUrl.value
    })

    const key = response.data.short_key
    shortenedUrl.value = `${window.location.origin}/${key}`
  } catch (err) {
    error.value = 'Ошибка: проверьте правильность URL'
    console.error(err)
  } finally {
    loading.value = false
  }
}
</script>


<style scoped>
.container { 
  max-width: 600px; 
  margin: 50px auto; 
  padding: 20px;
  text-align: center; 
  font-family: 'Inter', sans-serif; /* Современный шрифт */
  color: #2c3e50;
}

h1 { margin-bottom: 30px; color: #42b883; }

.input-group { display: flex; gap: 10px; margin-bottom: 20px; }

input { 
  flex: 1; 
  padding: 12px; 
  border: 2px solid #eee; 
  border-radius: 8px; 
  outline: none;
  transition: border-color 0.3s;
}

input:focus { border-color: #42b883; }

button { 
  padding: 10px 25px; 
  background: #42b883; 
  color: white; 
  border: none; 
  border-radius: 8px; 
  font-weight: bold;
  cursor: pointer; 
  transition: background 0.3s;
}

button:hover { background: #33a06f; }
button:disabled { background: #ccc; cursor: not-allowed; }

.result { 
  margin-top: 30px; 
  padding: 20px; 
  background: #f0fdf4; /* Светло-зеленый фон */
  border: 1px solid #bbf7d0; 
  border-radius: 12px; 
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

/* Исправление цвета текста здесь */
.result p { 
  margin: 0 0 10px 0; 
  color: #166534; /* Темно-зеленый текст, хорошо виден на светлом */
  font-weight: 600;
}

.result a { 
  color: #10b981; 
  font-weight: bold; 
  word-break: break-all;
  text-decoration: none;
  border-bottom: 2px dashed #10b981;
}

.error { 
  color: #dc2626; 
  background: #fee2e2;
  padding: 10px;
  border-radius: 8px;
  margin-top: 15px; 
}
</style>
