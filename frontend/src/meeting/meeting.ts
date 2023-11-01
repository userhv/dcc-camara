export class Meeting{
    static getMeetingWithID(allMeetings: Array<Array<any>>, meetingId: Number): Array<any>{
        for(let meeting of allMeetings){
            const [id, title, dateStr] = meeting;
            if(id == meetingId){
              return meeting
            }
        }
        return []
    }

    static getAgendasWithMeetingID(allAgendas: Array<Array<any>>, meetingId: Number): Array<Array<any>>{
        const result = []
        for(let agenda of allAgendas){
            const [titulo, reuniaoId, documento] = agenda;
            if(reuniaoId == meetingId){
                result.push(agenda)
            }
        }
        return result
    }
}

