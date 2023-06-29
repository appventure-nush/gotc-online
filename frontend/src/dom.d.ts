interface CustomEventMap {
    //contains the keys for our custom events
    //add more keys here with appropriate customevent type when creating more custom events
    //i think its best to emmit custom events on the document for ease of listening
    "SignInEvent": CustomEvent<string>;
    "SignOutEvent": CustomEvent;
}
declare global {
    //part of the stackoverflow answer i got. all i have to say is that it works
    interface Document { //adds definition to Document, but you can do the same with HTMLElement
        addEventListener<K extends keyof CustomEventMap>(type: K,
                                                         listener: (this: Document, ev: CustomEventMap[K]) => void): void;
        dispatchEvent<K extends keyof CustomEventMap>(ev: CustomEventMap[K]): void;
    }
}
export { }; //keep that for TS compiler.