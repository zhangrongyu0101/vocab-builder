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
function fetchSimilarWords() {
    return __awaiter(this, void 0, void 0, function* () {
        try {
            const response = yield fetch('/similar-words');
            const wordGroups = yield response.json();
            const container = document.getElementById('wordGroupsContainer');
            if (!container) {
                throw new Error('Container element not found');
            }
            // 清空现有内容
            container.innerHTML = '';
            // 遍历所有相似单词组并显示
            wordGroups.forEach((group) => {
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
// 在文档加载完成后获取相似单词组
document.addEventListener('DOMContentLoaded', fetchSimilarWords);
