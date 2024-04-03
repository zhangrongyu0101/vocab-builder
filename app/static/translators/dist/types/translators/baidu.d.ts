import { PronunciationSpeed, TranslationResult } from "../types";
/**
 * Baidu translator interface.
 */
declare class BaiduTranslator {
    MAX_RETRY: number;
    HOST: string;
    token: string;
    gtk: string;
    sign: string;
    languages: {};
    HEADERS: {
        accept: string;
        "accept-language": string;
        "content-type": string;
    };
    /**
     * Language to translator language code.
     */
    LAN_TO_CODE: Map<string, string>;
    /**
     * Translator language code to language.
     */
    CODE_TO_LAN: Map<string, string>;
    /**
     * TTS audio instance.
     */
    AUDIO: HTMLAudioElement;
    /**
     * Throw an error.
     *
     * @param code error code
     * @param msg error message
     * @param action action, enum{detect, translate, pronounce}
     * @param text text
     * @param from original language
     * @param to target language
     * @param error original error object
     *
     * @throws error
     */
    throwError(code: string, msg: string, action: string, text: string, from?: string | null, to?: string | null): never;
    /**
     * Get latest token and gtk for urls.
     *
     * @returns used to run callback. catch(error) used to catch error
     */
    getTokenGtk(): Promise<void>;
    /**
     * Parse the translate result.
     *
     * @param result translate result
     * @returns Parsed result
     */
    parseResult(result: any): TranslationResult;
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
     * @returns {Promise} then(result) used to return request result. catch(error) used to catch error
     */
    detect(text: string): Promise<string>;
    /**
     * Translate given text.
     *
     * @param text text to translate
     * @param from source language
     * @param to target language
     * @returns {Promise} then(result) used to return request result. catch(error) used to catch error
     */
    translate(text: string, from: string, to: string): Promise<TranslationResult>;
    /**
     * Pronounce given text.
     *
     * @param text text to pronounce
     * @param language language of text
     * @param speed "fast" or "slow"
     *
     * @returns {Promise<void>} pronounce finished
     */
    pronounce(text: string, language: string, speed: PronunciationSpeed): Promise<void>;
    /**
     * Pause pronounce.
     */
    stopPronounce(): void;
    tokenA(r: any, o: any): any;
    generateSign(query: any, gtk: any): string;
}
export default BaiduTranslator;
