import { PronunciationSpeed, TranslationResult } from "../types";
/**
 * Google translate interface.
 */
declare class GoogleTranslator {
    TKK: number[];
    HOME_PAGE: string;
    HOST: string;
    /**
     * Translate API.
     */
    TRANSLATE_URL: string;
    TTS_URL: string;
    /**
     * Fallback translate API.
     */
    FALLBACK_TRANSLATE_URL: string;
    FALLBACK_TTS_URL: string;
    /**
     * Should we fall back?
     */
    fallBacking: boolean;
    /**
     * Language to translator language code.
     */
    LAN_TO_CODE: Map<string, string>;
    /**
     * Translator language code to language.
     */
    CODE_TO_LAN: Map<string, string>;
    /**
     * Audio instance.
     */
    AUDIO: HTMLAudioElement;
    /**
     * Generate TK.
     *
     * @param a parameter
     * @param b parameter
     * @param c parameter
     *
     * @returns request TK
     */
    generateTK(a: any, b: any, c: any): string;
    /**
     * Generate magic number.
     *
     * @param a parameter
     * @param b parameter
     *
     * @returns magic number
     */
    _magic(a: any, b: any): any;
    /**
     * Update TKK from Google translate page.
     *
     * @returns promise
     */
    updateTKK(): Promise<void>;
    /**
     * Fall back to use old API and set a timeout to recover.
     */
    fallBack(): void;
    /**
     * Generate language detecting URL.
     *
     * @param text text to detect
     *
     * @returns the URL
     */
    generateDetectURL(text: string): string;
    /**
     * Generate translating URL.
     *
     * @param text text to translate
     * @param from source language
     * @param to target language
     *
     * @returns the URL
     */
    generateTranslateURL(text: string, from: string, to: string): string;
    /**
     * Parse detecting result.
     *
     * @param response detecting URL response
     *
     * @returns detected language
     */
    parseDetectResult(response: any): string;
    /**
     * Parse better Google translate result.
     *
     * @param response Google translate response
     *
     * @returns parsed result
     */
    parseBetterResult(response: any): TranslationResult;
    /**
     * Parse fallback Google translate result.
     *
     * @param response Google translate response
     *
     * @returns parsed result
     */
    parseFallbackResult(response: any): TranslationResult;
    /**
     * Parse Google translate result.
     *
     * @param response Google translate response
     *
     * @returns parsed result
     */
    parseTranslateResult(response: any): TranslationResult;
    /**
     * Get supported languages of this API.
     *
     * @returns supported languages
     */
    supportedLanguages(): Set<string>;
    /**
     * Detect the language of given text.
     *
     * @param text text to detect
     *
     * @returns detected language Promise
     */
    detect(text: string): Promise<string>;
    /**
     * Translate given text.
     *
     * @param text text to translate
     * @param from source language
     * @param to target language
     *
     * @returns {Promise<Object>} translation Promise
     */
    translate(text: string, from: string, to: string): Promise<TranslationResult>;
    /**
     * Pronounce text.
     *
     * @param text text to pronounce
     * @param language language of text
     * @param speed pronounce speed, "fast" or "slow"
     *
     * @returns Promise of playing
     */
    pronounce(text: string, language: string, speed: PronunciationSpeed): Promise<void>;
    /**
     * Stop pronouncing.
     */
    stopPronounce(): void;
}
export default GoogleTranslator;
