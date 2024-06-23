<template>
    <div>
      <button type="button" class="btn btn-primary" @click="showModal">
        Launch demo modal
      </button>
  
      <!-- Modal -->
      <div class="modal fade" ref="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="exampleModalLabel">Modal title</h5>
              <button type="button" class="btn-close" data-mdb-ripple-init data-mdb-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">...</div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-mdb-ripple-init data-mdb-dismiss="modal">Close</button>
              <button type="button" class="btn btn-primary" data-mdb-ripple-init>Save changes</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { Modal, Ripple, initMDB } from "mdb-ui-kit";
  
  export default {
    name: 'CampaignModal',
    mounted() {
      this.initMDBSetup();
    },
    methods: {
      initMDBSetup() {
        initMDB({ Modal, Ripple });
      },
      showModal() {
        var myModal = new Modal(this.$refs.exampleModal, {});
        myModal.show();
      }
    }
  }
  </script>
  