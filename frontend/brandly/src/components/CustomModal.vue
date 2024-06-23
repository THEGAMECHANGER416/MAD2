<template>
    <div v-if="visible" class="modal-overlay">
        <div class="modal-wrapper">
            <div class="modal-container">
                <div class="modal-header mb-0">
                    <slot name="header"></slot>
                    <button @click="close" class="btn-close mb-2"></button>
                </div>
                <hr class="hr my-0">
                <div class="modal-body my-0">
                    <slot name="body"></slot>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'CustomModal',
    props: {
        show: {
            type: Boolean,
            default: false
        }
    },
    data() {
        return {
            visible: this.show
        };
    },
    watch: {
        show(newValue) {
            this.visible = newValue;
        },
        visible(newValue) {
            this.$emit('update:show', newValue);
        }
    },
    methods: {
        close() {
            this.visible = false;
        }
    }
};
</script>

<style scoped>
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
}

.modal-wrapper {
    width: 100%;
    max-width: 600px;
    margin: 0 auto;
    margin-top: 3rem;
    background: white;
    border-radius: 8px;
    overflow: hidden;
}

.modal-header {
    padding: 1em;
    padding-bottom: 0.2em;
    background: white;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.modal-body {
    padding: 1em;
}

.modal-close {
    background: none;
    border: none;
    font-size: 1.5em;
    cursor: pointer;
}
</style>