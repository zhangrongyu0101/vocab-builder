interface WordGroup {
    words: string[];
    similarityType: string;
}

async function fetchSimilarWords(): Promise<void> {
    try {
        const response = await fetch('/similar-words');
        const wordGroups: WordGroup[] = await response.json();
        const container = document.getElementById('wordGroupsContainer');

        if (!container) {
            throw new Error('Container element not found');
        }

        // 清空现有内容
        container.innerHTML = '';

        // 遍历所有相似单词组并显示
        wordGroups.forEach((group: WordGroup) => {
            const groupDiv = document.createElement('div');
            groupDiv.className = 'word-group';
            groupDiv.textContent = `Words: ${group.words.join(', ')} (Type: ${group.similarityType})`;
            container.appendChild(groupDiv);
        });
    } catch (error) {
        console.error('Error fetching similar words:', error);
    }
}

// 在文档加载完成后获取相似单词组
document.addEventListener('DOMContentLoaded', fetchSimilarWords);
