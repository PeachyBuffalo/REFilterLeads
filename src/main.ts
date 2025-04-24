import { VerificationResult, Verification, HistoryResponse, VerificationFormData } from './types';

// Type declarations for DOM elements
interface DOMElements {
    verifyForm: HTMLFormElement | null;
    searchInput: HTMLInputElement | null;
    filterStatus: HTMLSelectElement | null;
    resultsDiv: HTMLDivElement | null;
    phoneResult: HTMLDivElement | null;
    emailResult: HTMLDivElement | null;
    riskResult: HTMLDivElement | null;
    verificationHistory: HTMLTableSectionElement | null;
    showingCount: HTMLElement | null;
    totalCount: HTMLElement | null;
    detailModal: HTMLDivElement | null;
    modalContent: HTMLDivElement | null;
    closeModal: HTMLElement | null;
    recentVerifications: HTMLTableSectionElement | null;
}

// Get DOM elements with type safety
const getDOMElements = (): DOMElements => ({
    verifyForm: document.getElementById('verifyForm') as HTMLFormElement,
    searchInput: document.getElementById('searchInput') as HTMLInputElement,
    filterStatus: document.getElementById('filterStatus') as HTMLSelectElement,
    resultsDiv: document.getElementById('results') as HTMLDivElement,
    phoneResult: document.getElementById('phoneResult') as HTMLDivElement,
    emailResult: document.getElementById('emailResult') as HTMLDivElement,
    riskResult: document.getElementById('riskResult') as HTMLDivElement,
    verificationHistory: document.getElementById('verificationHistory') as HTMLTableSectionElement,
    showingCount: document.getElementById('showingCount'),
    totalCount: document.getElementById('totalCount'),
    detailModal: document.getElementById('detailModal') as HTMLDivElement,
    modalContent: document.getElementById('modalContent') as HTMLDivElement,
    closeModal: document.getElementById('closeModal'),
    recentVerifications: document.getElementById('recentVerifications') as HTMLTableSectionElement
});

// Dashboard functionality
document.addEventListener('DOMContentLoaded', (): void => {
    const elements = getDOMElements();
    
    if (elements.verifyForm) {
        elements.verifyForm.addEventListener('submit', async (e: Event): Promise<void> => {
            e.preventDefault();
            
            const formData = new FormData(elements.verifyForm as HTMLFormElement);
            const data: VerificationFormData = {
                first_name: formData.get('first_name') as string,
                last_name: formData.get('last_name') as string,
                email: formData.get('email') as string,
                phone: formData.get('phone') as string
            };
            
            try {
                const response = await fetch('/api/verify', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
                
                const result: VerificationResult = await response.json();
                displayResults(result);
                await updateRecentVerifications();
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred while verifying the lead.');
            }
        });
    }
    
    // History page functionality
    if (elements.searchInput && elements.filterStatus) {
        elements.searchInput.addEventListener('input', debounce(updateHistory, 300));
        elements.filterStatus.addEventListener('change', updateHistory);
        
        // Initial load
        updateHistory();
    }
});

const displayResults = (result: VerificationResult): void => {
    const elements = getDOMElements();
    
    if (!elements.resultsDiv || !elements.phoneResult || !elements.emailResult || !elements.riskResult) return;
    
    elements.resultsDiv.classList.remove('hidden');
    
    // Phone verification results
    elements.phoneResult.innerHTML = `
        <div class="flex items-center">
            <span class="h-4 w-4 rounded-full ${result.phone_valid ? 'bg-green-400' : 'bg-red-400'}"></span>
            <span class="ml-2">${result.phone_valid ? 'Valid' : 'Invalid'}</span>
        </div>
        <div class="mt-2 text-sm text-gray-600">
            ${result.phone_details || ''}
        </div>
    `;
    
    // Email verification results
    elements.emailResult.innerHTML = `
        <div class="flex items-center">
            <span class="h-4 w-4 rounded-full ${result.email_valid ? 'bg-green-400' : 'bg-red-400'}"></span>
            <span class="ml-2">${result.email_valid ? 'Valid' : 'Invalid'}</span>
        </div>
        <div class="mt-2 text-sm text-gray-600">
            ${result.email_details || ''}
        </div>
    `;
    
    // Risk assessment results
    elements.riskResult.innerHTML = `
        <div class="flex items-center">
            <span class="h-4 w-4 rounded-full ${result.risk_score < 0.5 ? 'bg-green-400' : result.risk_score < 0.8 ? 'bg-yellow-400' : 'bg-red-400'}"></span>
            <span class="ml-2">Risk Score: ${(result.risk_score * 100).toFixed(1)}%</span>
        </div>
        <div class="mt-2 text-sm text-gray-600">
            ${result.risk_factors ? result.risk_factors.join(', ') : 'No risk factors identified'}
        </div>
    `;
};

const updateHistory = async (): Promise<void> => {
    const elements = getDOMElements();
    const searchTerm = elements.searchInput?.value || '';
    const statusFilter = elements.filterStatus?.value || '';
    
    try {
        const response = await fetch(`/api/history?search=${encodeURIComponent(searchTerm)}&status=${encodeURIComponent(statusFilter)}`);
        const data: HistoryResponse = await response.json();
        
        const verificationHistory = elements.verificationHistory;
        if (!verificationHistory) return;
        
        verificationHistory.innerHTML = '';
        
        data.verifications.forEach((verification: Verification) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td class="px-6 py-4 whitespace-nowrap">${verification.first_name} ${verification.last_name}</td>
                <td class="px-6 py-4 whitespace-nowrap">${verification.email}</td>
                <td class="px-6 py-4 whitespace-nowrap">${verification.phone}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                        ${verification.status === 'valid' ? 'bg-green-100 text-green-800' : 
                          verification.status === 'invalid' ? 'bg-red-100 text-red-800' : 
                          'bg-yellow-100 text-yellow-800'}">
                        ${verification.status}
                    </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">${(verification.risk_score * 100).toFixed(1)}%</td>
                <td class="px-6 py-4 whitespace-nowrap">${new Date(verification.timestamp).toLocaleString()}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <button onclick="showDetails(${verification.id})" class="text-indigo-600 hover:text-indigo-900">
                        Details
                    </button>
                </td>
            `;
            verificationHistory.appendChild(row);
        });
        
        if (elements.showingCount) elements.showingCount.textContent = data.verifications.length.toString();
        if (elements.totalCount) elements.totalCount.textContent = data.total.toString();
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while loading the history.');
    }
};

const showDetails = async (id: number): Promise<void> => {
    const elements = getDOMElements();
    if (!elements.detailModal) return;
    
    elements.detailModal.classList.remove('hidden');
    
    try {
        const response = await fetch(`/api/history/${id}`);
        const data: Verification = await response.json();
        
        if (!elements.modalContent) return;
        
        elements.modalContent.innerHTML = `
            <div class="space-y-4">
                <div>
                    <h4 class="font-medium">Verification Details</h4>
                    <pre class="mt-2 text-sm bg-gray-50 p-2 rounded">${JSON.stringify(data, null, 2)}</pre>
                </div>
            </div>
        `;
        
        if (elements.closeModal) {
            elements.closeModal.onclick = (): void => {
                elements.detailModal?.classList.add('hidden');
            };
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while loading verification details.');
    }
};

const debounce = <T extends (...args: any[]) => any>(func: T, wait: number): (...args: Parameters<T>) => void => {
    let timeout: NodeJS.Timeout;
    return function executedFunction(...args: Parameters<T>): void {
        const later = (): void => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
};

const updateRecentVerifications = async (): Promise<void> => {
    const elements = getDOMElements();
    
    try {
        const response = await fetch('/api/history?limit=5');
        const data: HistoryResponse = await response.json();
        
        const recentVerifications = elements.recentVerifications;
        if (!recentVerifications) return;
        
        recentVerifications.innerHTML = '';
        
        data.verifications.forEach((verification: Verification) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td class="px-6 py-4 whitespace-nowrap">${verification.first_name} ${verification.last_name}</td>
                <td class="px-6 py-4 whitespace-nowrap">${verification.email}</td>
                <td class="px-6 py-4 whitespace-nowrap">${verification.phone}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                        ${verification.status === 'valid' ? 'bg-green-100 text-green-800' : 
                          verification.status === 'invalid' ? 'bg-red-100 text-red-800' : 
                          'bg-yellow-100 text-yellow-800'}">
                        ${verification.status}
                    </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">${new Date(verification.timestamp).toLocaleString()}</td>
            `;
            recentVerifications.appendChild(row);
        });
    } catch (error) {
        console.error('Error:', error);
    }
}; 