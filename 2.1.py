import base64
import json
import random
from typing import List, Optional, Dict, Any

class Song:    
    def __init__(self, name: str, length: int, music_genre: str, score: float): #playlist класс
        if not name: raise ValueError("Название песни пустое:(")
        if length <= 0: raise ValueError("Длительность песни указана неверно:(")
        if not 0 <= score <= 10: raise ValueError("Рейтинг указан неверно:(")
        
        self.name = name
        self.length = length
        self.music_genre = music_genre
        self.score = score
    
    def to_json_dict(self) -> Dict[str, Any]: #словарь для простоты представления песен
        return {
            'name': self.name,
            'length': self.length,
            'music_genre': self.music_genre,
            'score': self.score
        }
    
    @classmethod
    def from_json_dict(cls, data: Dict[str, Any]) -> 'Song': #объект song из словаря
        return cls( name=data['name'], length=data['length'], music_genre=data['music_genre'], score=data['score'])
    
    def formatted_time(self) -> str: #вид времени
        minutes = self.length // 60
        seconds = self.length % 60
        return f"{minutes}:{seconds:02d}"
    
    def __str__(self) -> str: return f"{self.name} ({self.formatted_time()}) - {self.music_genre} {self.score:.1f}"
    def __repr__(self) -> str: return f"Song('{self.name}', {self.length}, '{self.music_genre}', {self.score})"


class MusicPlaylist: #класс для управления плейлистом
    
    def __init__(self, title: str = "Music Collection"):

        self.title = title
        self.songs: List[Song] = []
        self.loop_mode: str = 'off' #off, all, on
    
    def insert_song(self, song: Song) -> None: #добавление в конец

        if not isinstance(song, Song): raise TypeError("ОШИБКА.")
        self.songs.append(song)
    
    def delete_song(self, position: int) -> Optional[Song]: #удаление песен
        if not self.songs:
            print("Список песен пуст.")
            return None
        
        index = position - 1
        if not 0 <= index < len(self.songs):
            print(f"ОШИБКА В ИНДЕКСЕ.")
            return None
        return self.songs.pop(index)
    
    def delete_by_name(self, song_name: str) -> bool: #удаление песен по наименованию

        for idx, song in enumerate(self.songs):
            if song.name == song_name:
                self.songs.pop(idx)
                return True
        print("Такой песни нет.")
        return False
    
    def random_shuffle(self) -> None: #перемешка песен
        if not self.songs:
            return
        random.shuffle(self.songs)
    
    def change_loop_mode(self, mode: str) -> None: #РЕЖИМ ПОВТОРА
        if mode not in ['off', 'one', 'all']:
            raise ValueError("ОШИБКА РЕЖИМА.")
        self.loop_mode = mode
        print(f"Режим повтора изменён на: {self.loop_mode}")
    
    def save_playlist(self, file_path: str) -> None: #СОХРАНЕНИЕ плейлиста в текстовый файл (задание 1)*

        if not self.songs:
            print("Песен нет... Нечего сохранять:(")
            return
        
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                for song in self.songs:
                    json_str = json.dumps(song.to_json_dict(), ensure_ascii=False)
                    encoded = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
                    file.write(encoded + '\n')
            print(f"Плейлист сохранён в {file_path} ({len(self.songs)} песен)")
        except Exception as error:
            print("ОШИБКА.")
    
    def load_playlist(self, file_path: str) -> None: #загружает плейлист из файла
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.songs.clear()
                for line_number, line in enumerate(file, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        decoded = base64.b64decode(line.encode('utf-8')).decode('utf-8')
                        song_data = json.loads(decoded)
                        new_song = Song.from_json_dict(song_data)
                        self.songs.append(new_song)
                    except Exception as error:
                        print("ОШИБКА.")
            print(f"Загружено {len(self.songs)} песен из {file_path}")
        except FileNotFoundError:
            print("ОШИБКА. Такого файла нет.")
    
    def filter_by_genre(self, target_genre: str) -> List[Song]: # ФИЛЬТРАЦИЯ песен по жанру(задание 5)*
        if not self.songs:
            print("ПУСТО.")
            return []
        result = [song for song in self.songs if song.music_genre.lower() == target_genre.lower()]
        return result
    
    def display_all(self) -> None:
        if not self.songs:
            print("ПУСТО.")
            return
        
        print(f"\n{self.title}")
        print(f"Режим повтора: {self.loop_mode}")
        print(f"Всего песен: {len(self.songs)}\n")
        print("N  Название")
        print("-" * 62)
        for idx, song in enumerate(self.songs, start=1):
            print(f"{idx}  {song}")
        print()

def demonstration(): #ДЛЯ ДЕМОНСТРАЦИИ
    
    my_playlist = MusicPlaylist("ЛЮБИМЫЕ ПЕСНИ")

    print("НАЧАЛО ДЕМОНСТРАЦИИ.")
    print("="*30)
    print("\n1. ДОБАВЛЕНИЕ ПЕСЕН:") # 1.Добавление песен (другие названия)
    my_playlist.insert_song(Song("In the End", 216, "Rock", 6.6))
    my_playlist.insert_song(Song("Believer", 204, "Rock", 8.3))
    my_playlist.insert_song(Song("Shape of You", 233, "Pop", 9.4))
    my_playlist.insert_song(Song("See You Again", 235, "HipHop", 7.5))
    my_playlist.insert_song(Song("Counting Stars", 258, "PopRock", 3.2))
    print("Добавлено 5 песен")
    my_playlist.display_all()
    
    print("\n2. УДАЛЕНИЕ ПО ИНДЕКСУ (удаляем номер 3):")# 2.Удаление по индексу
    removed_song = my_playlist.delete_song(3)
    print(f"Удалено: {removed_song}")
    my_playlist.display_all()
    
    print("\n3. ПЕРЕМЕШИВАНИЕ:") # 3.Перемешка
    my_playlist.random_shuffle()
    my_playlist.display_all()
    
    print("\n4. РЕЖИМ ПОВТОРА:")     # 4.Режим повтора
    my_playlist.change_loop_mode('all')
    
    print("\n5. СОХРАНЕНИЕ ПЛЕЙЛИСТА В ФАЙЛ:") # 5.Сохранение в файл
    my_playlist.save_playlist('my_music.txt')
    
    print("\n6. ФИЛЬТРАЦИЯ ПО ЖАНРУ 'ROCK':") # 6.Фильтр по жанру
    rock_songs = my_playlist.filter_by_genre('Rock')
    print(f"НАЙДЕНО ПЕСЕН ПО ДАННОМУ ЖАНРУ: {len(rock_songs)}")
    for song in rock_songs:
        print(f"  - {song}")
    
    print("\n7. ЗАГРУЗКА ПЛЕЙЛИСТА ИЗ ФАЙЛА:") # 7.Загрузка из файла
    new_playlist = MusicPlaylist("ЗАГРУЖЕННЫЙ ПЛЕЙЛИСТ...")
    new_playlist.load_playlist('my_music.txt')
    new_playlist.display_all()
    
    print("\n8. ПРОВЕРКА ГРАНИЦ:")# 8. Проверка индивидуальных случаев
    
    print("\n   - Попытка удалить из пустого списка:")
    empty = MusicPlaylist("ТЕСТ")
    empty.delete_song(1)
    
    print("\n   - Попытка удалить с неверным индексом:")
    my_playlist.delete_song(46545)
    
    print("\n   - Фильтр по ошибочному жанру:")
    jazz = my_playlist.filter_by_genre('JAZZ')
    print(f"   НАЙДЕНО ПЕСЕН ПО ДАННОМУ ЖАНРУ: {len(jazz)}")
    
    print("\n   - Перемешка пустого плейлиста:")
    empty.random_shuffle() #т.е. ничего не происходит

    print("\n" + "="*30)
    print("КОНЕЦ ДЕМОНСТРАЦИИ.")

if __name__ == "__main__":
    demonstration()
