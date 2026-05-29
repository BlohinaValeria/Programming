import asyncio
from locust import FastHttpUser, task, between
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TeacherUser(FastHttpUser):
    wait_time = between(1, 3)
    host = "https://atlas.herzen.spb.ru"
    
    @task
    async def view_teachers_catalog(self):
        url = "/teachers"
        logger.info(f"Начинаю загрузку страницы: {url}")
        
        try:
            response = self.client.get(url)
            
            if response.status_code != 200:
                logger.error(f"Ошибка HTTP: статус {response.status_code} для URL {url}")
                return
            
            logger.info(f"Страница успешно загружена. Статус: {response.status_code}")
            
            html_content = response.text
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            teacher_elements = soup.find_all(class_='teacher-card')
            
            if not teacher_elements:
                teacher_elements = soup.find_all('article', class_='teacher-item')
            
            if not teacher_elements:
                logger.warning("Не удалось найти элементы с информацией о преподавателях. Проверьте селекторы.")
                return
            
            logger.info(f"Найдено {len(teacher_elements)} преподавателей. Начинаю асинхронную обработку...")
            
            tasks = []
            for teacher_element in teacher_elements:
                name_element = teacher_element.find('h3') or teacher_element.find(class_='name')
                full_name = name_element.get_text(strip=True) if name_element else "Не указано"
                
                tasks.append(self.process_teacher(full_name))
            
            await asyncio.gather(*tasks)
            
            logger.info("Завершена обработка всех преподавателей")
            
        except Exception as e:
            logger.error(f"Ошибка при выполнении запроса или обработке данных: {str(e)}")
    
    async def process_teacher(self, full_name: str):
        logger.info(f"Обработка преподавателя: {full_name}")
        await asyncio.sleep(0.1)
