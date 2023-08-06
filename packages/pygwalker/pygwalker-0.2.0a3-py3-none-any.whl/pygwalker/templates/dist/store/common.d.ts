interface IInitModalInfo {
    total: number;
    curIndex: number;
    title: string;
}
declare class CommonStore {
    initModalOpen: boolean;
    initModalInfo: IInitModalInfo;
    showCloudTool: boolean;
    setInitModalOpen(value: boolean): void;
    setInitModalInfo(info: IInitModalInfo): void;
    setShowCloudTool(value: boolean): void;
    constructor();
}
declare const commonStore: CommonStore;
export default commonStore;
