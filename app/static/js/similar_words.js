"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
function deleteWordGroup(groupId) {
    return __awaiter(this, void 0, void 0, function* () {
        openModal();
        try {
            fetch(`/delete/similar-words/${groupId}`, {
                method: 'DELETE',
            });
            closeModal();
            fetchSimilarWords();
            window.location.reload(); // 强制刷新页面
        }
        catch (error) {
            console.error('Error:', error);
            alert('Error deleting the word group');
        }
        window.location.reload();
    });
}
// 这个函数重新从后端加载并显示所有相似单词组
// async function fetchSimilarWords(): Promise<void> {
//     try {
//         const response = await fetch('/similar-words');
//         if (!response.ok) {
//             throw new Error(`HTTP error! status: ${response.status}`);
//         }
//         const wordGroups: SimilarWordGroup[] = await response.json();
//         const container = getElementById<HTMLDivElement>('wordGroupsContainer');
//         container.innerHTML = ''; // 清空现有内容
//         wordGroups.forEach(group => {
//             const groupDiv = document.createElement('div');
//             groupDiv.className = 'word-group';
//             groupDiv.textContent = `Words: ${group.words.join(', ')} (Type: ${group.similarityType})`;
//             container.appendChild(groupDiv);
//         });
//     } catch (error) {
//         console.error('Error fetching similar words:', error);
//     }
// }
function fetchSimilarWords() {
    fetch('/similar-words')
        .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
        .then((wordGroups) => {
        const container = getElementById('wordGroupsContainer');
        container.innerHTML = ''; // 清空现有内容
        wordGroups.forEach(group => {
            const groupDiv = document.createElement('div');
            groupDiv.className = 'word-group';
            groupDiv.textContent = `Words: ${group.words.join(',')} (Type: ${group.similarityType})`;
            container.appendChild(groupDiv);
        });
    })
        .catch(error => {
        console.error('Error fetching similar words:', error);
    });
}
// 获取元素的辅助函数，增加了类型断言
function getElementById(id) {
    const element = document.getElementById(id);
    if (!element)
        throw new Error(`Element with id ${id} not found`);
    return element;
}
function openModal() {
    const modal = getElementById('modal');
    modal.style.display = 'block';
}
function closeModal() {
    const modal = getElementById('modal');
    modal.style.display = 'none';
}
function fetchWordInfo(word) {
    fetch(`/get-word-info?word=${encodeURIComponent(word)}`)
        .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
        .then(data => {
        console.log('Word info:', data);
        // 在这里处理和显示单词信息
    })
        .catch(error => {
        console.error('Error fetching word info:', error);
    });
}
function playPronunciation(word) {
    const lang = 'en'; // 或根据需要调整语言
    const audioSrc = `/pronounce?text=${encodeURIComponent(word)}&lang=${lang}`;
    const audio = new Audio(audioSrc);
    audio.play().catch(error => console.error('Playback failed:', error));
}
// 绑定事件
document.addEventListener('DOMContentLoaded', () => {
    const addWordGroupBtn = getElementById('addWordGroupBtn');
    addWordGroupBtn.addEventListener('click', openModal);
});
