import { PronunciationSpeed, TranslationResult } from "../types";
/**
 * DeepL translator interface.
 */
declare class DeepLTranslator {
    /**
     * DeepL translate home page.
     */
    HOME_PAGE: string;
    /**
     * Language to translator language code.
     */
    LAN_TO_CODE: Map<string, string>;
    /**
     * Translator language code to language.
     */
    CODE_TO_LAN: Map<string, string>;
    langDetector: any;
    TTSEngine: any;
    deepLIframe: HTMLIFrameElement;
    constructor(langDetector: any, TTSEngine: any);
    /**
     * Create the iframe.
     */
    private createIframe;
    /**
     * Get supported languages of this API.
     *
     * @returns supported languages
     */
    supportedLanguages(): Set<string>;
    /**
     * Detect language of given text.
     *
     * @param text text to detect
     *
     * @returns detected language Promise
     */
    detect(text: string): Promise<any>;
    /**
     * Translate given text.
     *
     * @param text text to translate
     * @param from source language
     * @param to target language
     *
     * @returns translation Promise
     */
    translate(text: string, from: string, to: string): Promise<TranslationResult>;
    /**
     * Pronounce given text.
     *
     * @param text text to pronounce
     * @param language language of text
     * @param speed "fast" or "slow"
     *
     * @returns pronounce finished
     */
    pronounce(text: string, language: string, speed: PronunciationSpeed): Promise<any>;
    /**
     * Pause pronounce.
     */
    stopPronounce(): void;
}
export default DeepLTranslator;
