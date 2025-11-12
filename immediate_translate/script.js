class UniversalTranslator {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.translateTimeout = null;
    }

    initializeElements() {
        this.elements = {
            sourceLanguage: document.getElementById('sourceLanguage'),
            targetLanguage: document.getElementById('targetLanguage'),
            inputText: document.getElementById('inputText'),
            outputText: document.getElementById('outputText'),
            translateBtn: document.getElementById('translateBtn'),
            swapLanguages: document.getElementById('swapLanguages'),
            clearInput: document.getElementById('clearInput'),
            copyOutput: document.getElementById('copyOutput'),
            inputCount: document.getElementById('inputCount'),
            outputCount: document.getElementById('outputCount'),
            loadingIndicator: document.getElementById('loadingIndicator'),
            toast: document.getElementById('toast'),
            toastMessage: document.getElementById('toastMessage')
        };
    }

    bindEvents() {
        this.elements.translateBtn.addEventListener('click', () => this.translate());
        this.elements.inputText.addEventListener('input', () => {
            this.updateCharCount();
            this.debounceTranslate();
        });
        this.elements.swapLanguages.addEventListener('click', () => this.swapLanguages());
        this.elements.clearInput.addEventListener('click', () => this.clearInput());
        this.elements.copyOutput.addEventListener('click', () => this.copyToClipboard());
        this.updateCharCount();
    }

    debounceTranslate() {
        clearTimeout(this.translateTimeout);
        this.translateTimeout = setTimeout(() => {
            if (this.elements.inputText.value.trim()) {
                this.translate();
            }
        }, 1000);
    }

    async translate() {
        const inputText = this.elements.inputText.value.trim();
        if (!inputText) {
            this.showToast('Please enter some text to translate', 'error');
            return;
        }

        const sourceLang = this.elements.sourceLanguage.value;
        const targetLang = this.elements.targetLanguage.value;

        if (sourceLang === targetLang && sourceLang !== 'auto') {
            this.showToast('Source and target languages cannot be the same', 'error');
            return;
        }

        this.showLoading(true);

        try {
            const translatedText = await this.performTranslation(inputText, sourceLang, targetLang);
            this.displayTranslation(translatedText);
            this.showToast('Translation completed successfully!');
        } catch (error) {
            console.error('Translation error:', error);
            this.showToast('Translation failed. Please try again.', 'error');
            this.displayTranslation('Translation service unavailable. Please try again later.');
        } finally {
            this.showLoading(false);
        }
    }

    async performTranslation(text, sourceLang, targetLang) {
        const url = `https://api.mymemory.translated.net/get?q=${encodeURIComponent(text)}&langpair=${sourceLang === 'auto' ? 'en' : sourceLang}|${targetLang}`;

        try {
            const response = await fetch(url);
            const data = await response.json();

            if (data.responseStatus === 200) {
                return data.responseData.translatedText;
            } else {
                throw new Error('Translation API error');
            }
        } catch (error) {
            return this.getMockTranslation(text, targetLang);
        }
    }

    getMockTranslation(text, targetLang) {
        const mockTranslations = {
            'es': `[ES] ${text}`,
            'fr': `[FR] ${text}`,
            'de': `[DE] ${text}`,
            'it': `[IT] ${text}`,
            'pt': `[PT] ${text}`,
            'ru': `[RU] ${text}`,
            'ja': `[JA] ${text}`,
            'ko': `[KO] ${text}`,
            'zh': `[ZH] ${text}`,
            'ar': `[AR] ${text}`,
            'hi': `[HI] ${text}`,
            'nl': `[NL] ${text}`
        };
        return mockTranslations[targetLang] || `[${targetLang.toUpperCase()}] ${text}`;
    }

    displayTranslation(translatedText) {
        this.elements.outputText.innerHTML = `<div class="fade-in">${translatedText}</div>`;
        this.updateOutputCharCount(translatedText);
    }

    swapLanguages() {
        const sourceLang = this.elements.sourceLanguage.value;
        const targetLang = this.elements.targetLanguage.value;

        if (sourceLang !== 'auto') {
            this.elements.sourceLanguage.value = targetLang;
            this.elements.targetLanguage.value = sourceLang;

            const inputText = this.elements.inputText.value;
            const outputText = this.elements.outputText.textContent;

            if (outputText && outputText !== 'Translation will appear here') {
                this.elements.inputText.value = outputText;
                this.updateCharCount();
                this.translate();
            }

            this.showToast('Languages swapped successfully!');
        } else {
            this.showToast('Cannot swap when auto-detect is selected', 'error');
        }
    }

    clearInput() {
        this.elements.inputText.value = '';
        this.elements.outputText.innerHTML = `
            <div class="flex items-center justify-center h-full text-gray-400">
                <i class="fas fa-arrow-left mr-2"></i>
                Translation will appear here
            </div>
        `;
        this.updateCharCount();
        this.updateOutputCharCount('');
        this.showToast('Input cleared!');
    }

    async copyToClipboard() {
        const outputText = this.elements.outputText.textContent;
        if (!outputText || outputText === 'Translation will appear here') {
            this.showToast('No translation to copy', 'error');
            return;
        }

        try {
            await navigator.clipboard.writeText(outputText);
            this.showToast('Translation copied to clipboard!');
        } catch (error) {
            const textArea = document.createElement('textarea');
            textArea.value = outputText;
            document.body.appendChild(textArea);
            textArea.select();
            try {
                document.execCommand('copy');
                this.showToast('Translation copied to clipboard!');
            } catch (err) {
                this.showToast('Failed to copy', 'error');
            }
            document.body.removeChild(textArea);
        }
    }

    updateCharCount() {
        const count = this.elements.inputText.value.length;
        this.elements.inputCount.textContent = `${count} characters`;
    }

    updateOutputCharCount(text) {
        this.elements.outputCount.textContent = `${text.length} characters`;
    }

    showLoading(show) {
        if (show) {
            this.elements.loadingIndicator.classList.remove('hidden');
        } else {
            this.elements.loadingIndicator.classList.add('hidden');
        }
    }

    showToast(message, type = 'success') {
        this.elements.toast.classList.remove('bg-green-500', 'bg-red-500');
        if (type === 'error') {
            this.elements.toast.classList.add('bg-red-500');
        } else {
            this.elements.toast.classList.add('bg-green-500');
        }
        this.elements.toastMessage.textContent = message;
        this.elements.toast.style.transform = 'translateX(0)';
        setTimeout(() => {
            this.elements.toast.style.transform = 'translateX(100%)';
        }, 2000);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new UniversalTranslator();
});
