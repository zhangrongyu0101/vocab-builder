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
// 这个函数重新从后端加载并显示所有相似单词组
function fetchSimilarWords() {
    return __awaiter(this, void 0, void 0, function* () {
        try {
            const response = yield fetch('/similar-words');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const wordGroups = yield response.json();
            const container = getElementById('wordGroupsContainer');
            container.innerHTML = ''; // 清空现有内容
            wordGroups.forEach(group => {
                const groupDiv = document.createElement('div');
                groupDiv.className = 'word-group';
                groupDiv.textContent = `Words: ${group.words.join(', ')} (Type: ${group.similarityType})`;
                container.appendChild(groupDiv);
            });
        }
        catch (error) {
            console.error('Error fetching similar words:', error);
        }
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
function saveWords() {
    return __awaiter(this, void 0, void 0, function* () {
        const wordInput = getElementById('wordInput');
        const similarityTypeSelect = getElementById('similarityType');
        // 获取输入数据
        const words = wordInput.value.split(',');
        const similarityType = similarityTypeSelect.value;
        // 构造请求体
        const data = { words, similarityType };
        try {
            // 发送POST请求到后端
            const response = yield fetch('/api/similar-words', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            closeModal();
            yield fetchSimilarWords();
        }
        catch (error) {
            console.error('Error:', error);
        }
    });
}
function deleteWordGroup(groupId) {
    if (!groupId) {
        console.error('Group ID is required for delete operation');
        return;
    }
    try {
        const response = fetch(`/delete/similar-words/${groupId}`, {
            method: 'DELETE',
        });
        closeModal();
        fetchSimilarWords();
        // window.location.reload(); // 强制刷新页面
    }
    catch (error) {
        console.error('Error:', error);
        alert('Error deleting the word group');
    }
}
// 绑定事件
document.addEventListener('DOMContentLoaded', () => {
    const addWordGroupBtn = getElementById('addWordGroupBtn');
    addWordGroupBtn.addEventListener('click', openModal);
});
