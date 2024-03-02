interface SimilarWordsData {
    words: string[];
    similarityType: string;
}

interface SimilarWordGroup {
    _id: string;
    words: string[];
    similarityType: string;
}

// 这个函数重新从后端加载并显示所有相似单词组
async function fetchSimilarWords(): Promise<void> {
    try {
        const response = await fetch('/similar-words');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const wordGroups: SimilarWordGroup[] = await response.json();

        const container = getElementById<HTMLDivElement>('wordGroupsContainer');
        container.innerHTML = ''; // 清空现有内容

        wordGroups.forEach(group => {
            const groupDiv = document.createElement('div');
            groupDiv.className = 'word-group';
            groupDiv.textContent = `Words: ${group.words.join(', ')} (Type: ${group.similarityType})`;
            container.appendChild(groupDiv);
        });
    } catch (error) {
        console.error('Error fetching similar words:', error);
    }
}


// 获取元素的辅助函数，增加了类型断言
function getElementById<T extends HTMLElement>(id: string): T {
    const element = document.getElementById(id);
    if (!element) throw new Error(`Element with id ${id} not found`);
    return element as T;
}

function openModal(): void {
    const modal = getElementById<HTMLDivElement>('modal');
    modal.style.display = 'block';
}

function closeModal(): void {
    const modal = getElementById<HTMLDivElement>('modal');
    modal.style.display = 'none';
}

async function saveWords(): Promise<void> {
    const wordInput = getElementById<HTMLInputElement>('wordInput');
    const similarityTypeSelect = getElementById<HTMLSelectElement>('similarityType');
    
    // 获取输入数据
    const words = wordInput.value.split(',');
    const similarityType = similarityTypeSelect.value;

    // 构造请求体
    const data: SimilarWordsData = { words, similarityType };

    try {
        // 发送POST请求到后端
        const response = await fetch('/api/similar-words', {
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
        await fetchSimilarWords(); 
    } catch (error) {
        console.error('Error:', error);
    }
}

function deleteWordGroup(groupId: string) {
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
    } catch (error) {
        console.error('Error:', error);
        alert('Error deleting the word group');
    }
}

// 绑定事件
document.addEventListener('DOMContentLoaded', () => {
    const addWordGroupBtn = getElementById<HTMLButtonElement>('addWordGroupBtn');
    addWordGroupBtn.addEventListener('click', openModal);
});
