
class Annotation_dom {
    constructor(placeholder, logic, on_changed, required = false) {
        this.children = [];
        this.logic = logic;
        this.on_changed = on_changed;
        this.placeholder = placeholder;
        const input_type = logic.inputType;
        const key = logic.key;

        const key_node = document.createElement("div");
        key_node.innerHTML = (this.logic.key || "") + " [" + (input_type || "") + "]" + " (" + (logic.description || "") + ")";
        key_node.classList.add("key");
        placeholder.appendChild(key_node);

        this.value_node = document.createElement("div");
        this.value_node.classList.add("value");
        placeholder.appendChild(this.value_node);

        this.object = null;
        switch (input_type) {
            case "text":
                {
                    let input;
                    if (logic["metadata"] != null && logic["metadata"]["input"] != null && logic["metadata"]["input"] === "textarea") {
                        input = document.createElement("textarea");
                        input.setAttribute("cols", "40");
                        input.setAttribute("rows", "5");
                    } else {
                        input = document.createElement("input");
                        input.setAttribute("type", "text");
                    }
                    input.setAttribute("name", logic.key);
                    input.setAttribute("aria-label", logic.key);
                    this.value_node.appendChild(input);

                    logic.set_on_data(function(data) {
                        input.value = data;
                        this.placeholder.classList.add("selecting");
                    }.bind(this));
                    input.addEventListener('keydown', (event) => {
                        if(event.keyCode === 13) {                        
                            logic.set(input.value);
                            on_changed();
                        }
                    });

                    this.object = input;
                }
                break;
            case "mutual":
                {

                    const select = document.createElement("select");
                    select.setAttribute("name", logic.key);
                    select.setAttribute("aria-label", logic.key);
                    
                    while(select.firstChild) select.firstChild.remove();
                    let opt = document.createElement("option");
                    opt.value = ""; // the index
                    opt.innerHTML = "pick one";
                    select.append(opt);
                    logic.children.map((c, i) => {
                        opt = document.createElement("option");
                        opt.value = c.key;
                        opt.innerHTML = c.key;
                        select.append(opt);
                    });

                    this.value_node.appendChild(select);

                    logic.set_on_select(function(is_selected) {
                        let selected_child = null;
                        for (const child of logic.children) {
                            if (child.is_selected) {
                                selected_child = child;
                                break;
                            }
                        }
                        if (selected_child != null) {
                            select.value = selected_child.key;
                            this.clear(true);
                            if (selected_child.inputType != null) {
                                // populate ui
                                const div = document.createElement("div");
                                // change to after if you prefer a flat layout
                                this.value_node.appendChild(div);
                                this.children.push(new Annotation_dom(div, selected_child, on_changed, true));
                            }
                        }

                        if(is_selected) this.placeholder.classList.add("selecting");
                        else this.placeholder.classList.remove("selecting");
                    }.bind(this));
                    select.addEventListener('change', (event) => {
                        logic.set(select.value);
                        on_changed();
                    });

                    this.object = select;
                }
                break;
            case "property":
            case "multiple":
            default:
                {
                    const check = document.createElement("input");
                    check.type="checkbox";
                    check.setAttribute("name", logic.key);
                    check.setAttribute("aria-label", logic.key);
                    this.value_node.appendChild(check);

                    logic.set_on_select(function(is_selected) {
                        check.checked = is_selected;

                        if(is_selected)
                        {
                            if(logic.children != null) {                            
                                for (const c of logic.children) {
                                    const div = document.createElement("div");
                                    this.children.push(new Annotation_dom(div, c, on_changed, (c["required"] != null && c["required"])));   
                                    // change to after if you prefer a flat layout
                                    this.value_node.appendChild(div);
                                }
                            }
                            this.placeholder.classList.add("selecting");
                        }else{
                            this.clear(true);
                            this.placeholder.classList.remove("selecting");
                        }

                    }.bind(this));
                    check.addEventListener('change', (event) => {
                        if(check.checked) {
                            logic.set();
                        }else{
                            logic.unset();
                        }
                        on_changed();
                    });

                    this.object = check;
                }
                break;
        }

    }

    clear(leave_this = false) {
        if (!leave_this) {
            switch (this.logic.inputType) {
                case "text":
                    this.object.value = "";
                    break;
                case "property":
                    break;
                case "multiple":
                    break;
                case "mutual":
                    this.object.value = null;
                    break;
            }
        }

        for (const child of this.children) {
            child.clear();
            child.placeholder.remove();
        }
        this.children = [];
    }

    disable(flag) {
        switch (this.logic.inputType) {
            case "text":
                this.object.readOnly = flag;
                break;
            case "property":
                break;
            case "multiple":
                break;
            case "mutual":
                this.object.disabled = flag;
                break;
        }

        for (const child of this.children) {
            child.disable(flag);
        }
    }

}